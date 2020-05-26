# -*- encoding: utf-8 -*-
import abc
import base64
import json
import logging
import requests
import six
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from xml.dom.minidom import parseString
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class CASClient(object):
    '''
    A client for interacting with a remote CAS instance.

    ::

        >>> from cas_client import CASClient
        >>> client = CASClient('https://logmein.com')

    '''

    def __init__(
        self,
        server_url,
        service_url=None,
        auth_prefix='/cas',
        proxy_url=None,
        proxy_callback=None,
        verify_certificates=False,
        session_storage_adapter=None,
        headers=None,
    ):
        self._auth_prefix = auth_prefix
        self._proxy_callback = proxy_callback
        self._proxy_url = proxy_url
        self._server_url = server_url
        self._service_url = service_url
        self._session_storage_adapter = session_storage_adapter
        self._verify_certificates = bool(verify_certificates)
        self._headers = headers

    # PUBLIC METHODS

    def acquire_auth_token_ticket(self, headers=None):
        '''
        Acquire an auth token from the CAS server.
        '''
        logging.debug('[CAS] Acquiring Auth token ticket')
        url = self._get_auth_token_tickets_url()
        text = self._perform_post(url, headers=headers)
        auth_token_ticket = json.loads(text)['ticket']
        logging.debug('[CAS] Acquire Auth token ticket: {}'.format(
            auth_token_ticket))
        return auth_token_ticket

    def create_session(self, ticket, payload=None, expires=None):
        '''
        Create a session record from a service ticket.
        '''
        assert isinstance(self.session_storage_adapter, CASSessionAdapter)
        logging.debug('[CAS] Creating session for ticket {}'.format(ticket))
        self.session_storage_adapter.create(
            ticket,
            payload=payload,
            expires=expires,
        )

    def delete_session(self, ticket):
        '''
        Delete a session record associated with a service ticket.
        '''
        assert isinstance(self.session_storage_adapter, CASSessionAdapter)
        logging.debug('[CAS] Deleting session for ticket {}'.format(ticket))
        self.session_storage_adapter.delete(ticket)

    def get_api_url(
        self,
        api_resource,
        auth_token_ticket,
        authenticator,
        private_key,
        service_url=None,
        **kwargs
    ):
        '''
        Build an auth-token-protected CAS API url.
        '''
        auth_token, auth_token_signature = self._build_auth_token_data(
            auth_token_ticket,
            authenticator,
            private_key,
            **kwargs
        )
        params = {
            'at': auth_token,
            'ats': auth_token_signature,
        }
        if service_url is not None:
            params['service'] = service_url
        url = '{}?{}'.format(
            self._get_api_url(api_resource),
            urlencode(params),
        )
        return url

    def get_auth_token_login_url(
        self,
        auth_token_ticket,
        authenticator,
        private_key,
        service_url,
        username,
    ):
        '''
        Build an auth token login URL.

        See https://github.com/rbCAS/CASino/wiki/Auth-Token-Login for details.
        '''
        auth_token, auth_token_signature = self._build_auth_token_data(
            auth_token_ticket,
            authenticator,
            private_key,
            username=username,
        )
        logging.debug('[CAS] AuthToken: {}'.format(auth_token))
        url = self._get_auth_token_login_url(
            auth_token=auth_token,
            auth_token_signature=auth_token_signature,
            service_url=service_url,
        )
        logging.debug('[CAS] AuthToken Login URL: {}'.format(url))
        return url

    def get_destroy_other_sessions_url(self, service_url=None):
        '''
        Get the URL for a remote CAS `destroy-other-sessions` endpoint.

        ::

            >>> from cas_client import CASClient
            >>> client = CASClient('https://logmein.com')
            >>> service_url = 'http://myservice.net'
            >>> client.get_destroy_other_sessions_url(service_url)
            'https://logmein.com/cas/destroy-other-sessions?service=http://myservice.net'

        '''
        template = '{server_url}{auth_prefix}/destroy-other-sessions?service={service_url}'
        url = template.format(
            server_url=self.server_url,
            auth_prefix=self.auth_prefix,
            service_url=service_url or self.service_url,
        )
        logging.debug('[CAS] Login URL: {}'.format(url))
        return url

    def get_login_url(self, service_url=None):
        '''
        Get the URL for a remote CAS `login` endpoint.

        ::

            >>> from cas_client import CASClient
            >>> client = CASClient('https://logmein.com')
            >>> service_url = 'http://myservice.net'
            >>> client.get_login_url(service_url)
            'https://logmein.com/cas/login?service=http://myservice.net'

        '''
        template = '{server_url}{auth_prefix}/login?service={service_url}'
        url = template.format(
            server_url=self.server_url,
            auth_prefix=self.auth_prefix,
            service_url=service_url or self.service_url,
        )
        logging.debug('[CAS] Login URL: {}'.format(url))
        return url

    def get_logout_url(self, service_url=None):
        '''
        Get the URL for a remote CAS `logout` endpoint.

        ::

            >>> from cas_client import CASClient
            >>> client = CASClient('https://logmein.com')
            >>> service_url = 'http://myservice.net'
            >>> client.get_logout_url(service_url)
            'https://logmein.com/cas/logout?service=http://myservice.net'

        '''
        template = '{server_url}{auth_prefix}/logout?service={service_url}'
        url = template.format(
            server_url=self.server_url,
            auth_prefix=self.auth_prefix,
            service_url=service_url or self.service_url,
        )
        logging.debug('[CAS] Logout URL: {}'.format(url))
        return url

    def parse_logout_request(self, message_text):
        '''
        Parse the contents of a CAS `LogoutRequest` XML message.

        ::

            >>> from cas_client import CASClient
            >>> client = CASClient('https://logmein.com')
            >>> message_text = """
            ... <samlp:LogoutRequest
            ...     xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
            ...     xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
            ...     ID="935a2d0c-4026-481e-be3d-20a1b2cdd553"
            ...     Version="2.0"
            ...     IssueInstant="2016-04-08 00:40:55 +0000">
            ...     <saml:NameID>@NOT_USED@</saml:NameID>
            ...     <samlp:SessionIndex>ST-14600760351898-0B3lSFt2jOWSbgQ377B4CtbD9uq0MXR9kG23vAuH</samlp:SessionIndex>
            ... </samlp:LogoutRequest>
            ... """
            >>> parsed_message = client.parse_logout_request(message_text)
            >>> import pprint
            >>> pprint.pprint(parsed_message)
            {'ID': '935a2d0c-4026-481e-be3d-20a1b2cdd553',
             'IssueInstant': '2016-04-08 00:40:55 +0000',
             'Version': '2.0',
             'session_index': 'ST-14600760351898-0B3lSFt2jOWSbgQ377B4CtbD9uq0MXR9kG23vAuH',
             'xmlns:saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
             'xmlns:samlp': 'urn:oasis:names:tc:SAML:2.0:protocol'}

        '''
        result = {}
        xml_document = parseString(message_text)
        for node in xml_document.getElementsByTagName('saml:NameId'):
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    result['name_id'] = child.nodeValue.strip()
        for node in xml_document.getElementsByTagName('samlp:SessionIndex'):
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    result['session_index'] = str(child.nodeValue.strip())
        for key in xml_document.documentElement.attributes.keys():
            result[str(key)] = str(xml_document.documentElement.getAttribute(key))
        logging.debug('[CAS] LogoutRequest:\n{}'.format(
            json.dumps(result, sort_keys=True, indent=4, separators=[',', ': '])
        ))
        return result

    def perform_api_request(
        self,
        api_resource,
        auth_token_ticket,
        authenticator,
        private_key,
        method='POST',
        service_url=None,
        headers=None,
        **kwargs
    ):
        '''
        Perform an auth-token-protected request against a CAS API endpoint.
        '''
        assert method in ('GET', 'POST')
        url = self.get_api_url(
            api_resource,
            auth_token_ticket,
            authenticator,
            private_key,
            service_url=None,
            **kwargs
        )
        if method == 'GET':
            response = self._perform_get(url, headers=headers)
        elif method == 'POST':
            response = self._perform_post(url, headers=headers)
        return response

    def perform_proxy(self, proxy_ticket, headers=None):
        '''
        Fetch a response from the remote CAS `proxy` endpoint.
        '''
        url = self._get_proxy_url(ticket=proxy_ticket)
        logging.debug('[CAS] Proxy URL: {}'.format(url))
        return self._perform_cas_call(
            url,
            ticket=proxy_ticket,
            headers=headers,
        )

    def perform_proxy_validate(self, proxied_service_ticket, headers=None):
        '''
        Fetch a response from the remote CAS `proxyValidate` endpoint.
        '''
        url = self._get_proxy_validate_url(ticket=proxied_service_ticket)
        logging.debug('[CAS] ProxyValidate URL: {}'.format(url))
        return self._perform_cas_call(
            url,
            ticket=proxied_service_ticket,
            headers=headers,
        )

    def perform_service_validate(
        self,
        ticket=None,
        service_url=None,
        headers=None,
    ):
        '''
        Fetch a response from the remote CAS `serviceValidate` endpoint.
        '''
        url = self._get_service_validate_url(ticket, service_url=service_url)
        print("1: url = " + url)
        logging.debug('[CAS] ServiceValidate URL: {}'.format(url))
        return self._perform_cas_call(url, ticket=ticket, headers=headers)

    def session_exists(self, ticket):
        '''
        Test if a session records exists for a service ticket.
        '''
        assert isinstance(self.session_storage_adapter, CASSessionAdapter)
        exists = self.session_storage_adapter.exists(ticket)
        logging.debug('[CAS] Session [{}] exists: {}'.format(ticket, exists))
        return exists

    # PRIVATE METHODS #

    def _build_auth_token_data(
        self,
        auth_token_ticket,
        authenticator,
        private_key,
        **kwargs
    ):
        auth_token = dict(
            authenticator=authenticator,
            ticket=auth_token_ticket,
            **kwargs
        )
        auth_token = json.dumps(auth_token, sort_keys=True)
        if six.PY3:
            auth_token = auth_token.encode('utf-8')
        digest = SHA256.new()
        digest.update(auth_token)
        auth_token = base64.b64encode(auth_token)
        rsa_key = RSA.importKey(private_key)
        signer = PKCS1_v1_5.new(rsa_key)
        auth_token_signature = signer.sign(digest)
        auth_token_signature = base64.b64encode(auth_token_signature)
        return auth_token, auth_token_signature

    def _clean_up_response_text(self, response_text):
        lines = []
        for line in response_text.splitlines():
            line = line.rstrip()
            if line:
                lines.append(line)
        return '\n'.join(lines)

    def _get_api_url(self, api_resource):
        template = '{server_url}{auth_prefix}/api/{api_resource}'
        url = template.format(
            api_resource=api_resource,
            auth_prefix=self.auth_prefix,
            server_url=self.server_url,
        )
        return url

    def _get_auth_token_tickets_url(self):
        return self._get_api_url('auth_token_tickets')

    def _get_auth_token_login_url(self, auth_token, auth_token_signature, service_url):
        template = '{server_url}{auth_prefix}/authTokenLogin?{query_string}'
        query_string = urlencode({
            'at': auth_token,
            'ats': auth_token_signature,
            'service': service_url or self.service_url,
        })
        url = template.format(
            auth_prefix=self.auth_prefix,
            query_string=query_string,
            server_url=self.server_url,
        )
        return url

    def _get_proxy_url(self, ticket):
        template = '{server_url}{auth_prefix}/proxy?'
        template += 'targetService={proxy_callback}&pgt={ticket}'
        url = template.format(
            auth_prefix=self.auth_prefix,
            proxy_callback=self.proxy_callback,
            server_url=self.server_url,
            ticket=ticket,
        )
        return url

    def _get_proxy_validate_url(self, ticket):
        template = '{server_url}{auth_prefix}/proxy?'
        template += 'ticket={ticket}&service={proxy_callback}'
        url = template.format(
            auth_prefix=self.auth_prefix,
            proxy_callback=self.proxy_callback,
            server_url=self.server_url,
            ticket=ticket,
        )
        return url

    def _get_service_validate_url(self, ticket, service_url=None):
        template = '{server_url}{auth_prefix}/serviceValidate?'
        template += 'ticket={ticket}&service={service_url}'
        url = template.format(
            auth_prefix=self.auth_prefix,
            server_url=self.server_url,
            service_url=service_url or self.service_url,
            ticket=ticket,
        )
        if self.proxy_url:
            url = '{url}&pgtUrl={proxy_url}'.format(url, self.proxy_url)
        return url

    def _perform_cas_call(self, url, ticket, headers=None):
        if ticket is not None:
            logging.debug('[CAS] Requesting Ticket Validation')
            response_text = self._perform_get(url, headers=headers)
            response_text = self._clean_up_response_text(response_text)
            if response_text:
                logging.debug('[CAS] Response:\n{}'.format(response_text))
                return CASResponse(response_text)
        logging.debug('[CAS] Response: None')
        return None

    def _perform_get(self, url, headers=None):
        headers = headers or self.headers
        try:
            response = requests.get(
                url,
                verify=self.verify_certificates,
                headers=headers,
            )
            return response.text
        except requests.HTTPError:
            return None

    def _perform_post(self, url, headers=None):
        headers = headers or self.headers
        try:
            response = requests.post(
                url,
                verify=self.verify_certificates,
                headers=headers,
            )
            return response.text
        except requests.HTTPError:
            return None

    # PUBLIC PROPERTIES #

    @property
    def auth_prefix(self):
        '''
        The CAS client's auth prefix. Typically "/cas".
        '''
        return self._auth_prefix

    @property
    def headers(self):
        return self._headers

    @property
    def proxy_callback(self):
        '''
        The CAS client's proxy callback address.
        '''
        return self._proxy_callback

    @property
    def proxy_url(self):
        '''
        The CAS client's proxy URL.
        '''
        return self._proxy_url

    @property
    def server_url(self):
        '''
        The CAS client's CAS server URL (i.e. the server name of the CAS
        service).
        '''
        return self._server_url

    @property
    def service_url(self):
        '''
        The CAS client's default service URL.

        This can typically be overriden in any method call.
        '''
        return self._service_url

    @property
    def session_storage_adapter(self):
        '''
        The CAS client's session storage adapter for maintaining session state.
        '''
        return self._session_storage_adapter

    @property
    def verify_certificates(self):
        '''
        Flag for controlling whether the CAS client verifies SSL certificates
        in its ``requests`` calls.
        '''
        return self._verify_certificates


class CASResponse(object):
    '''
    A CAS response object.
    '''

    def __init__(self, response_text):
        self.response_text = response_text
        self.response_type, cas_data = self._parse_cas_xml_response(response_text)
        self.success = 'success' in self.response_type.lower()
        self.data = cas_data.get(self.response_type)
        if isinstance(self.data, dict):
            self.error = None
        else:
            self.data = {}
            self.error = cas_data
        self.user = self.data.get('user')
        self.attributes = self.data.get('attributes')

    @classmethod
    def _parse_cas_xml_response(cls, response_text):
        cas_type = 'noResponse'
        cas_data = {}
        if not response_text:
            return cas_type, cas_data
        xml_document = parseString(response_text)
        node_element = xml_document.documentElement
        if node_element.nodeName != 'cas:serviceResponse':
            raise Exception
        for child in node_element.childNodes:
            if child.nodeType != child.ELEMENT_NODE:
                continue
            cas_type = child.nodeName.replace("cas:", "")
            cas_data = cls._parse_cas_xml_data(child)
            break
        return cas_type, cas_data

    @classmethod
    def _parse_cas_xml_data(cls, xml_node, namespace='cas:'):
        result = {}
        tag_name = xml_node.nodeName
        if tag_name.startswith(namespace):
            tag_name = tag_name.replace(namespace, '')
        for child in xml_node.childNodes:
            if child.nodeType == child.TEXT_NODE:
                text = child.nodeValue.strip()
                if text:
                    result[tag_name] = text
            elif child.nodeType == child.ELEMENT_NODE:
                subresult = cls._parse_cas_xml_data(child)
                result.setdefault(tag_name, {}).update(subresult)
        return result


class CASSessionAdapter(object, metaclass=abc.ABCMeta):
    '''
    Abstract base class for session adapters.
    '''

    @abc.abstractmethod
    def create(self, ticket, payload=None, expires=None):
        '''
        Create a session identifier associated with ``ticket``.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, ticket):
        '''
        Destroy a session identifier associated with ``ticket``.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def exists(self, ticket):
        '''
        Test if a session identifier exists for ``ticket``.
        '''
        raise NotImplementedError


class MemcachedCASSessionAdapter(CASSessionAdapter):
    r'''A Memcached session adapter.'''

    def __init__(self, client):
        self._client = client

    def create(self, ticket, payload=None, expires=None):
        '''
        Create a session identifier in memcache associated with ``ticket``.
        '''
        if not payload:
            payload = True
        self._client.set(str(ticket), payload, expires)

    def delete(self, ticket):
        '''
        Destroy a session identifier in memcache associated with ``ticket``.
        '''
        self._client.delete(str(ticket))

    def exists(self, ticket):
        '''
        Test if a session identifier exists for ``ticket``.
        '''
        return self._client.get(str(ticket)) is not None


__all__ = [
    'CASClient',
    'CASResponse',
    'CASSessionAdapter',
    'MemcachedCASSessionAdapter',
]
