import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import App from './App.vue'
import './styles/global.css'

// 注册全局组件
import AppIcon from '@/components/icons/AppIcon.vue'

const app = createApp(App)

// 全局组件
app.component('AppIcon', AppIcon)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')