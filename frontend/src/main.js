import { createApp } from 'vue'
import { createWebHistory } from 'vue-router'

import createRouter from './pages/routes.js'
import App from './App.vue'

const router = createRouter(createWebHistory())

// Import our custom CSS
import './scss/styles.scss'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
library.add(fas, far)


/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Import only the Bootstrap components we need
import { Popover } from 'bootstrap';

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.mount('#app')

// Create an example popover
document.querySelectorAll('[data-bs-toggle="popover"]')
  .forEach(popover => {
    new Popover(popover)
  })
