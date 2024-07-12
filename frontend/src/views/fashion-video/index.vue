<template>
  <div class="home">
    <div class="floor">
      <div class="column_box" v-for="item in advInfos" :key="`${item.id}`">
        <img :src="item.object_url" />
        <p>{{ item.id }}</p>
        <!-- 点赞和收藏功能 -->
        <div class="actions">
          <span class="like" @click="like(item.id)">
            <i class="el-icon-thumb"></i> Like
          </span>
          <span class="favorite" @click="favorite(item.id)">
            <i class="el-icon-star-on"></i> Favorite
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 引入sortablejs
import Sortable from "sortablejs";
import * as fashionVideo from "@/api/fashionVideo";

export default {
  name: "home",
  data() {
    return {
      floorArr: ["王小虎1", "王小虎2", "王小虎3", "王小虎4"],
      advInfos: [],
    };
  },
  mounted() {
    //  拖拽事件一定要放在 mounted 生命周期内，因为这时真实的DOM才渲染出来
    this.rowDrop();
  },
  created: function () {
    this.getAdv();
  },
  methods: {
    // 行拖拽
    rowDrop() {
      const tbody = document.querySelector(".floor");
      const _this = this;
      Sortable.create(tbody, {
        onEnd({ newIndex, oldIndex }) {
          const currRow = _this.floorArr.splice(oldIndex, 1)[0];
          _this.floorArr.splice(newIndex, 0, currRow);
          // 截止上面为止，数组已经进行了更换，但是会看到视图没有更新，所以就进行了数组清空重新赋值
          const newArray = _this.floorArr.slice(0);
          _this.floorArr = [];
          _this.$nextTick(() => {
            _this.floorArr = newArray;
          });
        },
      });
    },
    getAdv() {
      fashionVideo.getAdv().then((response) => {
        this.advInfos = response.data.data.advInfo;
        console.log(response);
      });
    },
  },
};
</script>

<style>
.column_box {
  width: 100%;
  height: 100%;
  text-align: center;
  margin-bottom: 20px;
}
img {
  width: 60%;
}
</style>
