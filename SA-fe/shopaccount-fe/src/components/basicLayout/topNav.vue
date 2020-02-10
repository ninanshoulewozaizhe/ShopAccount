<template>
    <div class="nav_container">
      <div class="img_cut_container">
        <img class="app_icon" :src="appIcon" alt="app-icon">
      </div>
      <el-menu
        :default-active="'home'"
        class="topNav"
        mode="horizontal"
        router
        background-color="#20A4E5"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-menu-item index="home">首页</el-menu-item>
        <el-menu-item index="shops">店铺</el-menu-item>
        <el-menu-item index="salesStatus">销售情况</el-menu-item>
      </el-menu>
      <div class="user_container">
        <el-dropdown>
          <img class="user_avatar" :src="appIcon" />
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>个人中心</el-dropdown-item>
            <el-dropdown-item>退出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';

@Component({
  name: 'topNav'
})
export default class TopNav extends Vue {
  appIcon = AppIcon;
}
</script>

<style lang="scss" scoped>
.nav_container {
  display: flex;
  position: relative;
  flex-direction: row;
  height: 60px;
  background-color: #20A4E5;

  .img_cut_container {
    overflow: hidden;
    box-sizing: border-box;
    height: 60px;
    width: 60px;
    border: 5px solid #20A4E5;

    .app_icon {
      position: relative;
      top: -5px;
      left: -5px;
      height: 61px;
    }
  }

  .user_container {
    position: absolute;
    right: 10px;
    
    .user_avatar {
      height: 55px;
      border-radius: 50%;
    }
  } 
}

.el-dropdown-menu {
  text-align: center;
}
</style>