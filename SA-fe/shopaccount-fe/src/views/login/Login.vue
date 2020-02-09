<template>
  <div class="container_center">
    <h2>ShopAccount</h2>
    <!-- <div class="login_form" >
      <div class="data_input">
        <span class="pre_text">账号：</span>
        <el-input placeholder="请输入账号" v-model="username" clearable></el-input>
      </div>
      <div class="data_input">
        <span class="pre_text">密码：</span>
        <el-input placeholder="请输入密码" v-model="password" type="password" clearable></el-input>
      </div>
    </div> -->
    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="80px" class="login_ruleForm" v-if="loginState">
      <el-form-item label="账号" prop="username">
        <el-input v-model="ruleForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
      </el-form-item>
    </el-form>
    <!-- <div class="register_form" >
      <div class="data_input">
        <span class="pre_text">账号：</span>
        <el-input placeholder="请输入账号" v-model="username" clearable></el-input>
      </div>
      <div class="data_input">
        <span class="pre_text">密码：</span>
        <el-input placeholder="请输入密码" v-model="password" type="password" clearable></el-input>
      </div>
      <div class="data_input">
        <span class="pre_text">确认密码：</span>
        <el-input placeholder="请再次输入密码" v-model="confirmPd" type="password" clearable></el-input>
      </div>
    </div> -->
    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="80px" class="register_ruleForm" v-else>
      <el-form-item label="账号" prop="username">
        <el-input v-model="ruleForm.username"></el-input>
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

@Component
export default class HelloWorld extends Vue {
  ruleForm = {
    username: '',
    password: '',
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
    ]
  };
  loginState = true;
  registerText = '注册';
  submitText = '登录';

  register() {
    this.registerText = this.loginState ? '返回' : '注册';
    this.submitText = this.loginState ? '注册' : '登录';
    this.loginState = !this.loginState;
    this.informationClear();
  }

  submit() {
    const ruleForm: any = this.$refs.ruleForm;
    ruleForm.validate((vaild: boolean) => {
      if (vaild) {
        alert('submit!');
      } else {
        console.log('error submit!!');
        return false;
      }
    });
  }

  informationClear() {
    this.ruleForm = {
      username: '',
      password: '',
      confirmPd: ''
    };
    const ruleForm: any = this.$refs.ruleForm;
    ruleForm.resetFields();
  }

  checkUsername(rule: any, value: string, callback: any) {
    if (!value) {
      callback(new Error('账号不可空'));
    } else if (/^[A-Za-z0-9]{7,18}$/.test(value)) {
      callback();
    } else {
      callback(new Error('请输入7-18位的数字或字母组合'));
    }
  }

  validatePass(rule: any, value: string, callback: any) {
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
</style>