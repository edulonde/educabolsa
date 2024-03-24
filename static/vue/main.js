const app = Vue.createApp({
    data() {
        return {
            showMenu: false,
            showDropdownMenuConceitos: false,
            showDropdownAccount: false,



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