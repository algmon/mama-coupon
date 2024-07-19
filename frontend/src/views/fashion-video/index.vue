<template>
  <div class="home">
    <div class="floor">
      <div class="column_box" v-for="item in advInfos" :key="`${item.id}`">
        <!-- <img :src="item.object_url" /> -->
        <img src="../../../../backend/ads/Suanfamama_AIGC_Ad_0.png" style="width: 40%;" />
        <!-- <p>{{ item.id }}</p> -->
        <p>{{ item.adname }}</p>
        <span style="display: none" id="id">{{ item.id }}</span>
        <span>{{ item.content }}</span>
        <!-- 点赞和收藏功能 -->
        <div class="actions">
          <br />
          {{ item.like }}
          <span
            class="like"
            @click="like(item.id)"
            v-loading.fullscreen.lock="fullscreenLoading"
          >
            <i
              :class="['iconfont', 'icon-zan', { 'liked-icon': item.is_like }]"
              >{{ item.is_like ? "已赞" : "赞" }}</i
            >
          </span>
          <span class="dislike" @click="dislike(item.id)">
            {{ item.dislike }}
            <i
              :class="[
                'iconfont',
                'icon-xinsui',
                { 'disliked-icon': item.is_dislike },
              ]"
              >{{ item.is_dislike ? "已踩" : "踩" }}</i
            >
          </span>
          <!-- <span class="favorite" @click="favorite(item.id)">
            <i class="el-icon-star-on"></i> Favorite
          </span> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 引入sortablejs
import Sortable from "sortablejs";
import * as fashionVideo from "@/api/fashionVideo";
import { _ } from "core-js";

export default {
  name: "home",
  data() {
    return {
      floorArr: ["王小虎1", "王小虎2", "王小虎3", "王小虎4"],
      advInfos: [],
      fullscreenLoading: false,
      idArray: [],
    };
  },
  mounted() {
    //  拖拽事件一定要放在 mounted 生命周期内，因为这时真实的DOM才渲染出来
    // console.log('Component mounted');
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
          const idElements = tbody.querySelectorAll('span[id="id"]');
          _this.idArray = [];
          idElements.forEach((element) => {
            _this.idArray.push(element.textContent);
          });
          fashionVideo.dragAndDrop(_this.idArray).then((response) => {
            console.log(response);
          }).catch((error) => {
            console.error(error);
          });
          console.log(_this.idArray);
        },
      });
    },

    // 获取广告列表
    getAdv() {
      // console.count("getAdv called");
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      fashionVideo.getAdv().then((response) => {
        this.advInfos = response.data.data.advInfo;
        const like = response.data.data.like;
        const dislike = response.data.data.dislike;
        const adsList = response.data.data.ads_list;
        this.floorArr = adsList;
        localStorage.setItem("like", like);
        localStorage.setItem("dislike", dislike);
        for (let i = 0; i < response.data.data.advInfo.length; i++) {
          if (like != null) {
            for (let j = 0; j < like.length; j++) {
            if (response.data.data.advInfo[i].id == like[j]) {
              this.advInfos[i].is_like = true;
            }
          }
          }
          if (dislike != null) {
            for (let k = 0; k < dislike.length; k++) {
            if (response.data.data.advInfo[i].id == dislike[k]) {
              this.advInfos[i].is_dislike = true;
            }
          }
          }
        }
        loading.close();
        console.log(response);
      });
    },

    // 点赞
    like(id) {
      // console.log("点赞", id);
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      fashionVideo
        .like(id)
        .then(async (response) => {
          console.log(typeof response.data.code);
          if (response.data.code == 20000) {
            localStorage.setItem("like", response.data.data);
            await this.getAdv(); // 等待 getAdv 执行完毕
            // this.$message({
            //   message: "点赞成功",
            //   type: "success",
            // });
          } else {
            loading.close();
            this.$message.error("点赞失败");
          }
        })
        .catch((error) => {
          console.error(error);
          loading.close();
        });
    },

    // 不感兴趣
    dislike(id) {
      // console.log("点赞", id);
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      fashionVideo
        .dislike(id)
        .then(async (response) => {
          localStorage.setItem("dislike", response.data.data);
          console.log(typeof response.data.code);
          if (response.data.code == 20000) {
            await this.getAdv();
            // this.$message({
            //   message: "已踩",
            //   type: "success",
            // });
          } else {
            loading.close();
            this.$message.error("没有踩~");
          }
        })
        .catch((error) => {
          console.error(error);
          loading.close();
        });
    },
  },
};
</script>

<style>
@import "//at.alicdn.com/t/c/font_4622840_mz4gortkj2.css";

.column_box {
  width: 100%;
  height: 100%;
  text-align: center;
  margin-bottom: 20px;
}

img {
  width: 60%;
}

.like {
  margin: 8px;
  margin-left: -4px;
}

.dislike {
  margin: 8px;
}

.liked-icon {
  color: red;
}

.disliked-icon {
  color: #ccc;
}
</style>
