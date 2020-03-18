<template>
  <div>
    <h3>个人中心</h3>
    <div class="info_container">
      <div class="img_container">
        <img  class="avatar" :src="`/getImg?f=${user.img}&t=${Math.random()}`" alt="avatar">
        <el-upload
          class="avatar-uploader"
          action="/userImg"
          :show-file-list="false"
          :on-success="avatarUploadSuccess"
          :before-upload="beforeAvatarUpload">
          <el-button type="primary">更换头像</el-button>
        </el-upload>
      </div>
      <div class="detail_container">
        <el-form>
          <el-form-item label="账号：">
            <div>{{ user.username }}</div>
          </el-form-item>
          <el-form-item label="手机号码：">
            <div>{{ phoneDisplay }}</div>
          </el-form-item>
        </el-form>
        <div class="btn_container">
          <el-button class="btn_change_phone" @click="register">更换手机号码</el-button>
          <el-button class="btn_change_pd" @click="register">更改密码</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import { UserInfo } from '@/typing/profile/typings';
@Component({
  name: 'profile'
})
export default class Profile extends Vue {

  user: UserInfo = {
    username: 'test9527',
    phone: '13245698774',
    img: 'asd123456-shop-158382150436.png'
  };

  get phoneDisplay() {
    return this.user.phone.slice(0, 3) + '****' + this.user.phone.slice(7);
  }

  beforeAvatarUpload(file: any) {
    const isJPGorPNG = file.type === 'image/jpeg' || file.type === 'image/png';
    const isLt10M = file.size / 1024 / 1024 < 10;
    if (!isJPGorPNG) {
      this.$message.error('请上传jpg或png图片类型的文件');
      return false;
    }
    if (!isLt10M) {
      this.$message.error('上传头像图片大小不能超过 10MB');
      return false;
    }
    return isJPGorPNG && isLt10M;
  }

  avatarUploadSuccess(res: any) {
    console.log(res);
    this.user.img = res.data;
    console.log(this.user.img);
    this.$message.success('头像更换成功');
  }

}
</script>

<style lang="scss" scoped>
.info_container {
  display: flex;

  .img_container {
    text-align: center;
    margin-right: 30px;

    .avatar {
      width: 178px;
      height: 200px;
      margin-bottom: 20px;
      display: block;
      border-radius: 10px;
    }
  }

  .btn_container {
    position: relative;
    bottom: -20px;
  }
}


</style>