import { mount } from "@vue/test-utils";
import wavedrom from "@/components/utils/wavedrom";
import Vue from "vue";
import ElementUI from "element-ui";

Vue.use(ElementUI);

describe("wavedrom", () => {
  var msg = '<div id="wavedrom-error" style="">';
  const wrapper = mount(wavedrom, {
    props: {
      waveId: String,
      parentText: String,
      errorMessage: String,
    },
  });

  it("renders the correct markup: " + msg, () => {
    expect(wrapper.html()).toContain(msg);
    // expect(wrapper.text()).toMatch(msg);
  });

  it("has no button", () => {
    expect(wrapper.find("button").exists()).toBe(false);
  });

  // it('button should increment the count', () => {
  //   expect(wrapper.vm.count).toBe(0)
  //   const button = wrapper.find('button')
  //   button.trigger('click')
  //   expect(wrapper.vm.count).toBe(1)
  // })
});
