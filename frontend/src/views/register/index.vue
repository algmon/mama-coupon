<template>
  <div class="login-container">
    <el-form
      ref="registerForm"
      :model="registerForm"
      :rules="registerRules"
      class="login-form"
      autocomplete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">AIGC认知计算广告生成平台</h3>
        <h3 class="title">注册页</h3>
      </div>

      <!-- 用户名 -->
      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          v-model="registerForm.username"
          placeholder="用户名"
          name="username"
          type="text"
          tabindex="1"
          autocomplete="on"
        />
      </el-form-item>
      <!-- 密码 -->
      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          v-model="registerForm.password"
          :type="passwordType"
          placeholder="密码"
          name="password"
          tabindex="3"
          autocomplete="on"
          @keyup.enter.native="handleRegister"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon
            :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"
          />
        </span>
      </el-form-item>

      <!-- 密码二次确认 -->
      <el-form-item prop="confirmPassword">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          v-model="registerForm.confirmPassword"
          placeholder="确认密码"
          type="password"
          name="confirmPassword"
          tabindex="4"
          autocomplete="on"
        />
      </el-form-item>
      <!-- 邮箱 -->
      <el-form-item prop="email">
        <span class="svg-container">
          <svg-icon icon-class="email" />
        </span>
        <el-input
          v-model="registerForm.email"
          placeholder="邮箱"
          name="email"
          type="text"
          tabindex="2"
          autocomplete="on"
        />
      </el-form-item>
      <el-form-item prop="phone">
        <span class="svg-container">
          <i class="el-icon-phone" />
        </span>
        <el-input
          v-model="registerForm.phone"
          placeholder="手机号"
          name="phone"
          type="text"
          tabindex="3"
          autocomplete="on"
        />
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        style="width: 100%; margin-bottom: 30px"
        @click.native.prevent="handleRegister"
        >注册</el-button
      >

      <el-button
        :loading="loading"
        type="info"
        style="width: 100%; margin-bottom: 30px; margin-left: 0px"
        @click.native.prevent="handleLogin"
        >已有用户登录</el-button
      >
      
    </el-form>
  </div>
</template>

<script>
import { validUsername } from "@/utils/validate"; // 确保这个路径是 validate 函数的正确路径
import SvgIcon from "@/components/SvgIcon"; // 确保 SvgIcon 组件路径正确
import * as userApi from "@/api/user"; // 确保 SvgIcon 组件路径正确
export default {
  name: "Register",
  components: {
    SvgIcon,
  },
  data() {
    return {
      passwordType: "password",
      registerForm: {
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
      },
      registerRules: {
        username: [
          { required: true, trigger: "blur", validator: validUsername },
        ],
        email: [
          { required: true, message: "请输入邮箱地址", trigger: "blur" },
          {
            type: "email",
            message: "请输入有效的邮箱地址",
            trigger: ["blur", "change"],
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 6, message: "密码长度不能小于6位", trigger: "blur" },
        ],
        confirmPassword: [
          { required: true, message: "请确认密码", trigger: "blur" },
          { validator: this.confirmPasswordValidator, trigger: "blur" },
        ],
        phone: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          {
            pattern: /^1[3-9]\d{9}$/,
            message: "请输入有效的手机号",
            trigger: "blur",
          },
        ],
      },
      loading: false,
    };
  },
  methods: {
    showPwd() {
      // 显示或隐藏密码逻辑
    },
    handleLogin() {
      // this.$refs.loginForm.validate((valid) => {
      // if (valid) {
      this.loading = true;
      this.$store;
      this.$router.push({
        // path: this.redirect || "/",
        path: "/login",
        query: this.otherQuery,
      });
    },
    handleRegister() {
      // 注册逻辑
      userApi
        .register(this.registerForm)
        .then((response) => {
          console.log("12");
          this.$router.push({
            // path: this.redirect || "/",
            path: "/login",
            query: this.otherQuery,
          });
        })
        .catch((error) => {
          // 打印错误信息
          console.error("注册失败:" + error.response.data);

          // 检查错误响应中的状态码
          if (error.response && error.response.status === 501) {
            // 错误码为 501，提示手机号或邮箱已注册
            alert(error.response.data.detail);
          }
        });
    },
    confirmPasswordValidator(rule, value, callback) {
      if (value !== this.registerForm.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    },
  },
};
</script>
<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
