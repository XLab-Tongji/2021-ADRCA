<template>
    <div>
        <div class="login-wrap">
            <img src="../../public/logo.jpg" class="logo-login" width="100" height="100" alt="">
            <el-form @submit.native.prevent>
                <el-form-item>
                    <el-input type="text" :placeholder="'用户名'" v-model="username" autofocus clearable/>
                </el-form-item>
                <el-form-item>
                    <el-input type="password" :placeholder="'密码'" v-model="password" clearable/>
                </el-form-item>
                <el-form-item style="text-align: center">
                    <el-button type="primary" @click="login" round>
                        登录
                    </el-button>
                    <el-button type="text" @click.native="register">注册</el-button>
                </el-form-item>
            </el-form>

        </div>
    </div>
</template>
npu
<script>
    export default {
        name: "Login",
        data() {
            return {
                username: '',
                password: '',
            }
        },
        mounted() {
            // if (localStorage.getItem("mlabUser")) {
            //     this.$router.push('/');
            // }
        },
        methods: {
            login() {
               
                this.$axios({
                    method: "POST",
                    url: "/api/login",
                    data: {
                        username: this.username,
                        password: this.password
                    }
                }).then((response) => {
                   console.log(response)
                   if (response.data.res=="1"){
                       alert("登陆成功！")
                       this.$router.push('/show/show')
                   }
                   else if (response.data.res=="0"){
                       alert("输入密码不正确！");
                   } else {
                       alert("该用户名未注册！")
                   }
                  
                })
                console.log(this.username)
            },
            register() {
                this.$router.push('/registry')
            }
        }
    }
</script>

<style>
    .login-wrap {
        max-width: 320px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    .login-wrap:before {
        content: '';
        display: table;
    }

    .login-wrap:after {
        content: '';
        display: table;
        clear: both;
    }

    .logo-login {
        display: block;
        margin: 100px auto 50px auto;
    }
</style>
