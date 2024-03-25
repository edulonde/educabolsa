const app = Vue.createApp({
    data() {
        return {
            showMenu: false,
            showDropdownMenuConceitos: false,
            showDropdownAccount: false,
            showConceitosBasicos_01: false,
            showConceitosBasicos_02: false,
            showConceitosBasicos_03: false,
            showConceitosBasicos_04: false,
            showConceitosBasicos_05: false,




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