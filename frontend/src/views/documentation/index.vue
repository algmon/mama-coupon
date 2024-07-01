<template>
  <div class="app-container documentation-container">
    <el-row :gutter="20">
      <el-col
        :span="8"
      ><div class="grid-content bg-purple">
        <a
          class="document-btn"
          target="_blank"
          href="g"
        >Suanfamama Official Website</a>
      </div>
      </el-col>
      <el-col
        :span="8"
      ><div class="grid-content bg-purple">
        <a
          class="document-btn"
          target="_blank"
          href="https://www.suanfamama.com/docs/research/intro"
        >妈妈技术解读</a>
      </div></el-col>
      <el-col
        :span="8"
      ><div class="grid-content bg-purple">
        <a
          class="document-btn"
          target="_blank"
          href="https://panjiachen.github.io/vue-element-admin-site/"
        >Frontend Docs</a>
      </div></el-col>
      <el-col
        :span="8"
      ><div class="grid-content bg-purple">
        <a
          class="document-btn"
          target="_blank"
          href="https://github.com/PanJiaChen/vue-element-admin/"
        >Frontend Docs</a>
      </div></el-col>
      <el-col
        :span="8"
      ><div class="grid-content bg-purple">
        <a
          class="document-btn"
          target="_blank"
          href="https://github.com/PanJiaChen/vue-element-admin/"
        >Frontend Docs</a>
      </div></el-col>
      <el-col
        :span="8"
      ><div class="grid-content bg-purple">
        <dropdown-menu
          class="document-btn"
          :items="articleList"
          title="系列前端技术文章"
        /></div></el-col>
    </el-row>

    <!-- 确保 iframe 填满整个 .el-col-24 -->
    <iframe
      class="full-screen-iframe"
      src="https://huggingface.co/spaces/weijiang2024/Suanfamama_AIGC_alg1"
      width="800px"
    />
    <iframe
      class="full-screen-iframe"
      src="https://huggingface.co/spaces/weijiang2024/Suanfamama_AIGC_alg3"
      width="800px"
    />
  </div>
</template>

<script>
import DropdownMenu from '@/components/Share/DropdownMenu'

export default {
  name: 'Documentation',
  components: { DropdownMenu },
  data() {
    return {
      articleList: [
        {
          title: '基础篇',
          href: 'https://juejin.im/post/59097cd7a22b9d0065fb61d2'
        },
        {
          title: '登录权限篇',
          href: 'https://juejin.im/post/591aa14f570c35006961acac'
        },
        {
          title: '实战篇',
          href: 'https://juejin.im/post/593121aa0ce4630057f70d35'
        },
        {
          title: 'vue-admin-template 篇',
          href: 'https://juejin.im/post/595b4d776fb9a06bbe7dba56'
        },
        {
          title: 'v4.0 篇',
          href: 'https://juejin.im/post/5c92ff94f265da6128275a85'
        },
        {
          title: '自行封装 component',
          href: 'https://segmentfault.com/a/1190000009090836'
        },
        {
          title: '优雅的使用 icon',
          href: 'https://juejin.im/post/59bb864b5188257e7a427c09'
        },
        {
          title: 'webpack4（上）',
          href: 'https://juejin.im/post/59bb864b5188257e7a427c09'
        },
        {
          title: 'webpack4（下）',
          href: 'https://juejin.im/post/5b5d6d6f6fb9a04fea58aabc'
        }
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
.documentation-container {
  margin: 50px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;

  .document-btn {
    flex-shrink: 0;
    display: block;
    cursor: pointer;
    background: black;
    color: white;
    height: 60px;
    padding: 0 16px;
    margin: 16px;
    line-height: 60px;
    font-size: 20px;
    text-align: center;
  }
  .el-row {
    display: flex; /* 启用 Flexbox */
    margin-left: 200px;
    justify-content: center; /* 水平居中 */
    height: 100%; /* 确保 .el-row 占满其父容器的高度 */
  }

  /* 全屏 iframe 类 */
  .full-screen-iframe {
    width: 100%;
    height: 600px;
  }
}
</style>
