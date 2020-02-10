<template>
    <el-container>
    <el-header>
        <top-nav></top-nav>
    </el-header>
    <el-main>
        <router-view></router-view>
    </el-main>
    </el-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import topNav from '../components/basicLayout/topNav.vue';

@Component({
  name: 'basicLayout',
  components: {
      topNav
  }
})
export default class BasicLayout extends Vue {

}
</script>

<style lang="scss" scoped>

</style>