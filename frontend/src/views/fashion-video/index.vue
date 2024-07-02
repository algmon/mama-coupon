<template>
  <ul class="video-list">
    <li v-for="video in videos" :key="video.id">
      <video :src="video.url" controls />
      <p>{{ video.title }}</p>
    </li>
  </ul>
</template>

<script>
export default {
  data() {
    return {
      videos: [],
      page: 1,
      isLoading: false,
    };
  },
  mounted() {
    this.fetchVideos();
  },
  methods: {
    fetchVideos() {
      if (this.isLoading) return;
      this.isLoading = true;
      videoService.getVideos(this.page).then((response) => {
        this.videos.push(...response.data.videos);
        this.page += 1;
        this.isLoading = false;
      });
    },
    handleScroll() {
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        this.fetchVideos();
      }
    },
  },
};
</script>

<style scoped>
.video-list video {
  width: 100%;
}
/* 其他样式 */
</style>
