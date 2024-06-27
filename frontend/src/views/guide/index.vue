<template>
  <div class="app-container">
    <aside>
      The product guide page is useful for users who login to the AIGC platform for the first time. We briefly introduce the
      core features of the products here step by step.
    </aside>
    <el-button icon="el-icon-question" type="primary" @click.prevent.stop="guide">
      Show Product Guide
    </el-button>
  </div>
</template>

<script>
import Driver from 'driver.js' // import driver.js
import 'driver.js/dist/driver.min.css' // import driver.js css
import steps from './steps'

export default {
  name: 'Guide',
  data() {
    return {
      driver: null
    }
  },
  mounted() {
    this.driver = new Driver()
  },
  methods: {
    guide() {
      this.driver.defineSteps(steps)
      this.driver.start()
    }
  }
}
</script>
