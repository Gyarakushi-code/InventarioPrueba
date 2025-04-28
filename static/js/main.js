$(document).ready(function(){
	/*Mostrar ocultar area de notificaciones*/
	$('.btn-Notification').on('click', function(){
        var ContainerNoty=$('.container-notifications');
        var NotificationArea=$('.NotificationArea');
        if(NotificationArea.hasClass('NotificationArea-show')&&ContainerNoty.hasClass('container-notifications-show')){
            NotificationArea.removeClass('NotificationArea-show');
            ContainerNoty.removeClass('container-notifications-show');
        }else{
            NotificationArea.addClass('NotificationArea-show');
            ContainerNoty.addClass('container-notifications-show');
        }
    });
    /*Mostrar ocultar menu principal*/
    $('.btn-menu').on('click', function(){
    	var navLateral=$('.navLateral');
    	var pageContent=$('.pageContent');
    	var navOption=$('.navBar-options');
    	if(navLateral.hasClass('navLateral-change')&&pageContent.hasClass('pageContent-change')){
    		navLateral.removeClass('navLateral-change');
    		pageContent.removeClass('pageContent-change');
    		navOption.removeClass('navBar-options-change');
    	}else{
    		navLateral.addClass('navLateral-change');
    		pageContent.addClass('pageContent-change');
    		navOption.addClass('navBar-options-change');
    	}
    });
    /*Salir del sistema*/
    document.getElementById('btn-logout').addEventListener('click', function () {
        Swal.fire({
            title: '¿Deseas cerrar sesión?',
            text: 'Serás redirigido al inicio de sesión.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, salir',
            cancelButtonText: 'Cancelar',
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6'
        }).then((result) => {
            if (result.isConfirmed) {
                // Redirige a la ruta /logout que debe cerrar la sesión
                window.location.href = '/logout';
            }
        });
    });
    /*Mostrar y ocultar submenus*/
    $('.btn-subMenu').on('click', function(){
    	var subMenu=$(this).next('ul');
    	var icon=$(this).children("span");
    	if(subMenu.hasClass('sub-menu-options-show')){
    		subMenu.removeClass('sub-menu-options-show');
    		icon.addClass('zmdi-chevron-left').removeClass('zmdi-chevron-down');
    	}else{
    		subMenu.addClass('sub-menu-options-show');
    		icon.addClass('zmdi-chevron-down').removeClass('zmdi-chevron-left');
    	}
    });
});
(function($){
    $(window).load(function(){
        $(".navLateral-body, .NotificationArea, .pageContent").mCustomScrollbar({
            theme:"dark-thin",
            scrollbarPosition: "inside",
            autoHideScrollbar: true,
            scrollButtons:{ enable: true }
        });
    });
})(jQuery);

function ordenarTabla() {
    const filtro = document.getElementById('filtro').value;
    const table = document.querySelector("table tbody");
    const rows = Array.from(table.querySelectorAll("tr"));

    let index = filtro.includes("nombre") ? 0 : 1;

    rows.sort((a, b) => {
        const aText = a.children[index].innerText.toLowerCase();
        const bText = b.children[index].innerText.toLowerCase();

        if (filtro.includes("fecha")) {
            const dateA = new Date(aText);
            const dateB = new Date(bText);
            return filtro === "fecha-asc" ? dateA - dateB : dateB - dateA;
        } else {
            return filtro === "nombre-asc"
                ? aText.localeCompare(bText)
                : bText.localeCompare(aText);
        }
    });

    rows.forEach(row => table.appendChild(row));
}