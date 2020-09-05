import { mount } from "@vue/test-utils";
import homepage from "@/components/main";
import Vue from "vue";
import ElementUI from "element-ui";

Vue.use(ElementUI);

describe("homepage", () => {
  const wrapper = mount(homepage);

  var msg = '本服务综合了不同难度的数字电路设计问题，适合各种水平的数字电路学习者。您输入的 Verilog 模块将会通过一系列向量，并与标准模块对应的输出来评价您实现的正确性';
  it("renders the correct markup: " + msg, () => {
    expect(wrapper.html()).toContain(msg);
    expect(wrapper.text()).toMatch(msg);
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
