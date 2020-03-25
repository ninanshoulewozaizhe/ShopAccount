<template>
    <el-container>
    <el-header>
        <top-nav :image="userImg"></top-nav>
    </el-header>
    <el-main>
        <router-view @updateAvatar="updateAvatar"></router-view>
    </el-main>
    </el-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import topNav from '../components/basicLayout/topNav.vue';
import store from '@/store';
import { UIMG, LOAD_USER_PROFILE} from '@/store/modules/user/constants';

@Component({
  name: 'basicLayout',
  components: {
      topNav
  },
  async beforeRouteEnter(to: any, from: any, next: any) {
    await store.dispatch(`user/${LOAD_USER_PROFILE}`);
    next();
  }
})
export default class BasicLayout extends Vue {

  userImg = '';

  mounted() {
    this.getUserImg();
  }

  updateAvatar() {
    this.getUserImg();
  }

  getUserImg() {
    const userImg = store.getters[`user/${UIMG}`];
    this.userImg = userImg;
    console.log(this.userImg);
  }
}
</script>

<style lang="scss" scoped>

</style>