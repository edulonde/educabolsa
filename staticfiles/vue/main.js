const app = Vue.createApp({
    data() {
        return {
            showMenu: false,
            showDropdownAccount: false,
            testevue: 'Teste Vue',

        }
    },
    methods: {
        toggleDropdownAccount() {
            this.showDropdownAccount = !this.showDropdownAccount
        },
    }
}
)

app.mount('#app')