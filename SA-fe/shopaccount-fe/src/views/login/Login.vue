<template>
  <div class="container_center">
    <h2>ShopAccount</h2>
    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="80px" class="login_ruleForm" v-if="loginState">
      <el-form-item label="账号" prop="username">
        <el-input v-model="ruleForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
      </el-form-item>
    </el-form>
    <el-form :model="ruleForm" :rules="rules" 
    ref="ruleForm" label-width="80px" 
    class="register_ruleForm" v-else>
      <el-form-item label="账号" prop="username">
        <el-input v-model="ruleForm.username"></el-input>
      </el-form-item>
      <el-form-item label="手机号码" prop="phone">
        <el-input v-model="ruleForm.phone"></el-input>
      </el-form-item>
      <el-form-item label="验证码">
        <el-input class="Vcode_input"></el-input>
        <el-button type="primary">发送验证码</el-button>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPd">
        <el-input type="password" v-model="ruleForm.confirmPd" autocomplete="off"></el-input>
      </el-form-item>
    </el-form>
    <div class="btn_container">
      <el-button class="btn_register" @click="register">{{ registerText }}</el-button>
      <el-button class="btn_sumit" @click="submit">{{ submitText }}</el-button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { SignUpForm, LoginForm } from '@/typing/login/typings';
import { SIGNUP, LOGIN, CHECK_USERNAME_EXIST, CHECK_PHONE_EXIST } from '../../store/modules/user/constants';

@Component({
  name: 'login'
})
export default class Login extends Vue {
  ruleForm: SignUpForm = {
    username: '',
    password: '',
    phone: '',
    confirmPd: ''
  };
  rules = {
    username: [
      { validator: this.checkUsername, trigger: 'blur' }
    ],
    password: [
      { validator: this.validatePass, trigger: 'blur' }
    ],
    confirmPd: [
      { validator: this.confirmPass, trigger: 'blur' }
    ],
    phone: [
      { validator: this.checkPhone, trigger: 'blur' }
    ]
  };
  loginState = true;
  formState = false;
  registerText = '注册';
  submitText = '登录';

  register() {
    this.registerText = this.loginState ? '返回' : '注册';
    this.submitText = this.loginState ? '注册' : '登录';
    this.loginState = !this.loginState;
    this.informationClear();
  }

  async submit() {
    if (this.loginState) {
      const loginForm: LoginForm = {
        username: this.ruleForm.username,
        password: this.ruleForm.password
      };
      const fields = Object.freeze({ ...loginForm });
      const result = await this.$store.dispatch(`user/${LOGIN}`, fields);
      if (result !== 'OK') {
        this.$notify.error({
          title: '登录失败',
          message: '请输入正确的账号或者密码'
        });
      } else {
        this.$notify({
            title: '登录成功',
            message: '欢迎回来',
            type: 'success'
        });
        this.$router.push({ name: 'home' });
      }
    } else {
      const ruleForm: any = this.$refs.ruleForm;
      ruleForm.validate(async (success: boolean) => {
        if (!success) {
          this.$notify.error({
            title: '注册失败',
            message: '请填好注册信息'
          });
        } else {
          const fields = Object.freeze({ ...this.ruleForm });
          const result = await this.$store.dispatch(`user/${SIGNUP}`, fields);
          if (result !== 'OK') {
            this.$notify.error({
              title: '注册失败',
              message: '请稍后重试'
            });
          } else {
            this.$notify({
              title: '注册成功',
              message: '恭喜成为本站成员',
              type: 'success'
            });
            this.register();
          }
        }
      });
    }
  }

  informationClear() {
    this.ruleForm = {
      username: '',
      password: '',
      phone: '',
      confirmPd: ''
    };
    const ruleForm: any = this.$refs.ruleForm;
    ruleForm.resetFields();
  }

  async checkUsername(rule: any, value: string, callback: any) {
    if (this.loginState) {
      callback();
      return;
    }
    if (!value) {
      callback(new Error('账号不可空'));
    } else if (/^[A-Za-z0-9]{7,18}$/.test(value)) {
      const result = await this.$store.dispatch(`user/${CHECK_USERNAME_EXIST}`, value);
      if (result === 'exist') {
        callback();
      } else {
        callback(new Error('账号已存在，请更换账号'));
      }
    } else {
      callback(new Error('请输入7-18位的数字或字母组合'));
    }
  }

  validatePass(rule: any, value: string, callback: any) {
    if (this.loginState) {
      callback();
      return;
    }
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
    } else if (value === this.ruleForm.password) {
      callback();
    } else {
      callback(new Error('两次输入的密码不同'));
    }
  }

  async checkPhone(rule: any, value: string, callback: any) {
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

  formValidate(success: boolean) {
    this.formState = success;
    console.log(this.formState);
  }
}

</script>

<style lang="scss" scoped>
.container_center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  .el-form {
    margin-left: -45px;
  }

  .btn_container {
    width: 200px;
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
  }
}

.el-input {
  width: 250px;
}

.Vcode_input {
  width: 120px;
  margin-right: 10px;
}
</style>