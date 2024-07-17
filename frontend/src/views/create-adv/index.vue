<template>
  <div>
    广告主 创建 广告界面
    <el-input v-model="issue" placeholder="请输入内容" />

    <el-input v-model="answer" type="textarea" :rows="2" placeholder="算法妈妈智聊" />
    <el-button type="primary" round @click="getAnswer">算法妈妈智聊</el-button>
  </div>
</template>

<script>
import * as chat from "@/api/aiChat";

export default {
  name: "AiChat",
  data() {
    return {
      issue: "",
      answer: "",
    };
  },
  methods: {
    getAnswer() {
      var data = { issue: this.issue };
      chat.fetchAnswer(data).then((response) => {
        this.answer = response.data.answer;
        console.log(response);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.multiline-input {
  // white-space: normal; /* 自动换行 */
  /* 可选：如果希望显示垂直滚动条而不是自动换行 */
  white-space: nowrap;
  overflow-y: auto;
}
</style>
