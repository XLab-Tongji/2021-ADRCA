import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Index from './views/Index.vue'
import Login from './views/Login.vue'
import Registry from './views/Register.vue'
Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/show',
            redirect: '/show/show',
            name: 'mainpage',
           
            component: () => import( /* webpackChunkName: "about" */ './views/MainPage.vue'),
            children: [
                {
                    path: 'test',
                    name: 'test',
                    component: () => import('./views/dygraph/dy.vue'),
                },
                // {
                //     path: 'import',
                //     name: 'import',
                //     component: () => import('./views/import/Import.vue'),
                // },
                {
                    path: 'show',
                    name: 'show',
                    component: () => import('./views/showData/test.vue'),
                }
                // {
                //     path: 'overview',
                //     name: 'SystemOverview',
                //     component: () => import('./views/KnowledgeGraph/SystemOverview.vue'),

                // },
                // {
                //     path: 'service',
                //     name: 'ServiceCall',
                //     component: () => import('./views/KnowledgeGraph/ServiceCall.vue'),
                // },
                // {
                //     path: 'timestamp',
                //     name: 'EventTimeStamp',
                //     component: () => import('./views/KnowledgeGraph/EventTimeStamp.vue'),
                // }
            ]
        },
        {
            path: '/zoom',
            name: '/zoom',
            component: () => import('./components/zoomcircle/Zoomable.vue'),
        },
        {
            path: '/',
            name: 'Index',
            component: Index
          },
          {
            path: '/show2',
            name: 'Show2',
            redirect: '/show2/show',
            component: () => import( /* webpackChunkName: "about" */ './views/MainPage.vue'),
            children: [
                {
                    path: 'test',
                    name: 'test',
                    component: () => import('./views/dygraph/dy.vue'),
                },
                // {
                //     path: 'import',
                //     name: 'import',
                //     component: () => import('./views/import/Import.vue'),
                // },
                {
                    path: 'show',
                    name: 'show',
                    component: () => import('./views/showData/test.vue'),
                }
                // {
                //     path: 'overview',
                //     name: 'SystemOverview',
                //     component: () => import('./views/KnowledgeGraph/SystemOverview.vue'),

                // },
                // {
                //     path: 'service',
                //     name: 'ServiceCall',
                //     component: () => import('./views/KnowledgeGraph/ServiceCall.vue'),
                // },
                // {
                //     path: 'timestamp',
                //     name: 'EventTimeStamp',
                //     component: () => import('./views/KnowledgeGraph/EventTimeStamp.vue'),
                // }
            ]
          },
          {
            path: '/login',
            name: 'Login',
            component: Login
          },
          {
            path: '/registry',
            name: 'Registry',
            component: Registry
          },
    ]
})