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
          <el-button class="btn_change_phone" @click="updatePhoneDialog = true">更换手机号码</el-button>
          <el-button class="btn_change_pd" @click="updatePasswordDialog = true">更改密码</el-button>
        </div>
        <el-dialog class="info_dialog" title="更换手机号码" :visible.sync="updatePhoneDialog">
          <el-form :rules="rules">
            <el-form-item label="原手机号码">
              <el-input disabled v-model="phoneDisplay"></el-input>
            </el-form-item>
            <el-form-item label="新手机号码" prop="phone">
              <el-input v-model="newPhone"></el-input>
            </el-form-item>
          </el-form>
          <footer>
            <el-button @click="updatePhoneDialog = false">取消</el-button>
            <el-button @click="updatePhoneDialog = false">确定</el-button>
          </footer>
        </el-dialog>
        <el-dialog class="info_dialog" title="更换密码" :visible.sync="updatePasswordDialog">
          <el-form :model="newPasswordForm" :rules="rules">
            <el-form-item label="原密码">
              <el-input type="password" v-model="newPasswordForm.o_password"></el-input>
            </el-form-item>
            <el-form-item label="新密码" prop="password">
              <el-input type="password" v-model="newPasswordForm.n_password" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPd">
              <el-input type="password" v-model="newPasswordForm.n_confirmPd" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <footer>
            <el-button @click="updatePasswordDialog = false">取消</el-button>
            <el-button @click="updatePasswordDialog = false">确定</el-button>
          </footer>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppIcon from '../../../public/images/accountBook.jpg';
import { UserInfo, ChangePdForm } from '@/typing/profile/typings';
import store from '@/store';
import { CURRENT_USER_INFO, LOAD_USER_PROFILE, CHECK_PHONE_EXIST } from '@/store/modules/user/constants';

@Component({
  name: 'profile',
  async beforeRouteEnter(to: any, from: any, next: any) {
    await store.dispatch(`user/${LOAD_USER_PROFILE}`);
    const userInfo = store.getters[`user/${CURRENT_USER_INFO}`];
    next((vm: any) => {
      vm.user = { ...userInfo };
    });
  }
})
export default class Profile extends Vue {
  user: UserInfo = {
    id: -1,
    username: '',
    phone: '',
    img: ''
  };

  updatePhoneDialog = false;
  updatePasswordDialog = false;

  newPasswordForm: ChangePdForm = {
    o_password: '',
    n_password: '',
    n_confirmPd: ''
  };

  newPhone = '';

  rules = {
    phone: [
      { validator: this.checkPhone, trigger: 'blur' }
    ],
    password: [
      { validator: this.validatePass, trigger: 'blur' }
    ],
    confirmPd: [
      { validator: this.confirmPass, trigger: 'blur' }
    ]
  };

  async checkPhone(rule: any, value: string, callback: any) {
    console.log(value);
    value = value.replace(/(^\+86|^86)/, '').replace(/-/g, '').trim();
    if (!value) {
      callback(new Error('请输入手机'));
    } else if (/^1[3-9]\d{9}$/.test(value)) {
      const result = await this.$store.dispatch(`user/${CHECK_PHONE_EXIST}`, value);
      if (result === 'exist') {
        callback();
      } else {
        callback(new Error('该手机号已被使用，请更换手机号码'));
      }
    } else {
      callback(new Error('请输入正确的手机号码'));
    }
  }

  validatePass(rule: any, value: string, callback: any) {
    console.log(value);
    if (!value) {
      callback(new Error('密码不可空'));
    } else if (/^[A-Za-z0-9]{7,18}$/.test(value)) {
      callback();
    } else {
      callback(new Error('请输入7-18位的数字或字母组合'));
    }
  }

  confirmPass(rule: any, value: string, callback: any) {
    if (!value) {
      callback(new Error('请再次输入密码'));
    } else if (value === this.newPasswordForm.o_password) {
      callback();
    } else {
      callback(new Error('两次输入的密码不同'));
    }
  }

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