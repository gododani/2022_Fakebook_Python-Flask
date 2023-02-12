/* ==================== SIDEBAR ==================== */

const menuItems = document.querySelectorAll('.menu-item');

// Remove active class from all menu items
const changeActiveItem = () =>{
    menuItems.forEach(item => {
        item.classList.remove('active');
    })
}

// Add active class to item and popup
menuItems.forEach(item =>{
    item.addEventListener('click', () => {
        changeActiveItem();
        item.classList.add('active');
        // if (item.id != 'notifications'){
        //     document.querySelector('.notifications-popup').style.display = 'none';
        // } else {
        //     document.querySelector('.notifications-popup').style.display = 'block';
        //     document.querySelector('#notifications .notification-count').style.display = 'none';
        // }
    })
})


/* ==================== LOGIN MODAL ==================== */


/* === MODAL ===*/


const reg_login = document.querySelector('#reg-login');
const loginModal = document.querySelector('.modal-login');

// opens modal
const openLoginModal = () =>{
    loginModal.style.display = 'grid';
    registerModal.style.display = 'none'
}

// closes modal
const closeLoginModal = (e) =>{
    if(e.target.classList.contains('modal-login')){
        loginModal.style.display = 'none';
    }
}

// open modal
reg_login.addEventListener('click', openLoginModal);

// close modal
loginModal.addEventListener('click', closeLoginModal);

if(document.querySelector('#login') != null){
    const login = document.querySelector('#login');
    // open modal
    login.addEventListener('click', openLoginModal);
}



/* ==================== REGISTER MODAL ==================== */


/* === MODAL ===*/

const register = document.querySelector('#register');
const registerModal = document.querySelector('.modal-register');

// opens modal
const openRegisterModal = () =>{
    registerModal.style.display = 'grid';
    loginModal.style.display = 'none';
}

// closes modal
const closeRegisterModal = (e) =>{
    if(e.target.classList.contains('modal-register')){
        registerModal.style.display = 'none';
    }
}

// open modal
register.addEventListener('click', openRegisterModal);

// close modal
registerModal.addEventListener('click', closeRegisterModal);


/* ==================== HOME ==================== */


if(document.querySelector('#home') != null){
    const home = document.querySelector('#home');
    home.addEventListener('click', () => {
        document.querySelector('.middle-home').style.display = 'initial';
        document.querySelector('#add_friend').style.display = 'none';
        document.querySelector('.middle-friends').style.display = 'none';
        document.querySelector('#create_group').style.display = 'none';
        document.querySelector('.middle-groups').style.display = 'none';
        document.querySelector('#upload_img').style.display = 'none';
        document.querySelector('.middle-images').style.display = 'none';
        document.querySelector('#create_album').style.display = 'none';
        document.querySelector('.middle-albums').style.display = 'none';
    })
}



/* ==================== FRIENDS ==================== */


if(document.querySelector('#friends') != null){
    const friends = document.querySelector('#friends');
    friends.addEventListener('click', () => {
        document.querySelector('.middle-home').style.display = 'none';
        document.querySelector('#add_friend').style.display = 'flex';
        if(screen.width <= 650){
            document.querySelector('.middle-friends').style.display = 'flex';
        } else{
            document.querySelector('.middle-friends').style.display = 'grid';
        }
        document.querySelector('#create_group').style.display = 'none';
        document.querySelector('.middle-groups').style.display = 'none';
        document.querySelector('#upload_img').style.display = 'none';
        document.querySelector('.middle-images').style.display = 'none';
        document.querySelector('#create_album').style.display = 'none';
        document.querySelector('.middle-albums').style.display = 'none';
    })
}



/* ==================== GROUPS ==================== */


if(document.querySelector('#groups') != null){
    const groups = document.querySelector('#groups');
    groups.addEventListener('click', () => {
        document.querySelector('.middle-home').style.display = 'none';
        document.querySelector('#add_friend').style.display = 'none';
        document.querySelector('.middle-friends').style.display = 'none';
        document.querySelector('#create_group').style.display = 'flex';
        if(screen.width <= 650){
            document.querySelector('.middle-groups').style.display = 'flex';
        } else{
            document.querySelector('.middle-groups').style.display = 'grid';
        }
        document.querySelector('#upload_img').style.display = 'none';
        document.querySelector('.middle-images').style.display = 'none';
        document.querySelector('#create_album').style.display = 'none';
        document.querySelector('.middle-albums').style.display = 'none';
    })
}



/* ==================== IMAGES ==================== */


if(document.querySelector('#images')){
    const images = document.querySelector('#images');
    images.addEventListener('click', () => {
        document.querySelector('.middle-home').style.display = 'none';
        document.querySelector('#add_friend').style.display = 'none';
        document.querySelector('.middle-friends').style.display = 'none';
        document.querySelector('#create_group').style.display = 'none';
        document.querySelector('.middle-groups').style.display = 'none';
        document.querySelector('#upload_img').style.display = 'flex';
        if(screen.width <= 650){
            document.querySelector('.middle-images').style.display = 'flex';
        } else{
            document.querySelector('.middle-images').style.display = 'grid';
        }
        document.querySelector('#create_album').style.display = 'none';
        document.querySelector('.middle-albums').style.display = 'none';
    })
}



/* ==================== ALBUMS ==================== */


if(document.querySelector('#albums')){
    const albums = document.querySelector('#albums');
    albums.addEventListener('click', () => {
        if (document.querySelector('.middle-home') != null){
            document.querySelector('.middle-home').style.display = 'none';
        }
        if(document.querySelector('#add_friend') != null){
            document.querySelector('#add_friend').style.display = 'none';
        }
        if (document.querySelector('.middle-friends') != null){
            document.querySelector('.middle-friends').style.display = 'none';
        }
        if (document.querySelector('#create_group') != null){
            document.querySelector('#create_group').style.display = 'none';
        }
        if (document.querySelector('.middle-groups') != null){
            document.querySelector('.middle-groups').style.display = 'none';
        }
        if (document.querySelector('#upload_img') != null){
            document.querySelector('#upload_img').style.display = 'none';
        }
        if (document.querySelector('.middle-images') != null){
            document.querySelector('.middle-images').style.display = 'none';
        }
        if (document.querySelector('#create_album') != null){
            document.querySelector('#create_album').style.display = 'flex';
        }
        if (document.querySelector('.middle-albums') != null){
            if(screen.width <= 650){
                document.querySelector('.middle-albums').style.display = 'flex';
            } else{
                document.querySelector('.middle-albums').style.display = 'grid';
            }
        }
    })
}



/* ==================== MESSAGES ==================== */


const messagesNotification = document.querySelector('#messages-notifications');

if(document.querySelector('#message-search') != null){
    const messageSearch = document.querySelector('#message-search');
    if(document.querySelector('.messages') != null){
        const messages = document.querySelector('.messages');
        if(messages.querySelectorAll('.message') != null){
            const message = messages.querySelectorAll('.message');
            // Chat searching function
            const searchMessage = () => {
                const val = messageSearch.value.toLowerCase();
                message.forEach(user => {
                    let name = user.querySelector('h5').textContent.toLowerCase();
                    if(name.indexOf(val) != -1){
                        user.style.display = 'flex';
                    } else{
                        user.style.display = 'none';
                    }
                })
            }
            // Search chat
            messageSearch.addEventListener('keyup', searchMessage);
        }
        // Highlight messages when messages menu item is clicked
        messagesNotification.addEventListener('click', () => {
            messages.style.boxShadow = '0 0 1rem var(--color-primary)';
            messagesNotification.querySelector('.notification-count').style.display = 'none';
            setTimeout(() => {
                messages.style.boxShadow = 'none';
            }, 1500);
        })
    }
}





// Category active class
const messageCategorys = document.querySelectorAll('.message-bar .category h6');

// Remove active class from all object
const changeActiveCategory = () =>{
    messageCategorys.forEach(item => {
        item.classList.remove('active');
    })
}

// Add active class to clicked object
messageCategorys.forEach(item =>{
    item.addEventListener('click', () => {
        changeActiveCategory();
        item.classList.add('active');
        // Personal
        if(document.querySelector('.personal-messages') != null){
            if(item.id != 'personal-chat'){
                document.querySelector('.personal-messages').style.display = 'none';
            } else{
                document.querySelector('.personal-messages').style.display = 'block';
            }
        }
        if(document.querySelector('.group-messages') != null){
            if(item.id != 'group-chat'){
                document.querySelector('.group-messages').style.display = 'none';
            } else{
                document.querySelector('.group-messages').style.display = 'block';
            }
        }
        if(document.querySelector('.request-messages') != null){
            if(item.id != 'request-chat'){
                document.querySelector('.request-messages').style.display = 'none';
            } else{
                document.querySelector('.request-messages').style.display = 'block';
            }
        }
    })
})


/* ==================== CREATE POST ==================== */


if(document.querySelector('#create-post-notification') != null && document.querySelector('#create-post-notification2') != null){
    const createPostNotification = document.querySelector('#create-post-notification');
    const createPostNotification2 = document.querySelector('#create-post-notification2');
    const post = document.querySelector('.c-post');
    
    createPostNotification.addEventListener('click', () => {
        changeActiveItem()
        document.querySelector('#home').classList.add('active');
        document.querySelector('.middle-home').style.display = 'initial';
        document.querySelector('#add_friend').style.display = 'none';
        document.querySelector('.middle-friends').style.display = 'none';
        document.querySelector('#create_group').style.display = 'none';
        document.querySelector('.middle-groups').style.display = 'none';
        document.querySelector('#upload_img').style.display = 'none';
        document.querySelector('.middle-images').style.display = 'none';
        document.querySelector('#create_album').style.display = 'none';
        document.querySelector('.middle-albums').style.display = 'none';
        post.style.boxShadow = '0 0 1rem var(--color-primary)';
        setTimeout(() => {
            post.style.boxShadow = 'none';
        }, 1500);
    })
    
    createPostNotification2.addEventListener('click', () => {
        changeActiveItem()
        document.querySelector('#home').classList.add('active');
        document.querySelector('.middle-home').style.display = 'initial';
        document.querySelector('#add_friend').style.display = 'none';
        document.querySelector('.middle-friends').style.display = 'none';
        document.querySelector('#create_group').style.display = 'none';
        document.querySelector('.middle-groups').style.display = 'none';
        document.querySelector('#upload_img').style.display = 'none';
        document.querySelector('.middle-images').style.display = 'none';
        document.querySelector('#create_album').style.display = 'none';
        document.querySelector('.middle-albums').style.display = 'none';
        post.style.boxShadow = '0 0 1rem var(--color-primary)';
        setTimeout(() => {
            post.style.boxShadow = 'none';
        }, 1500);
    })
}



/* ==================== THEME CUSTOMIZATION MODAL ==================== */


/* === MODAL ===*/
if(document.querySelector('#theme') != null ){
    const theme = document.querySelector('#theme');
    const themeModal = document.querySelector('.modal-theme');

// opens modal
const openThemeModal = () =>{
    themeModal.style.display = 'grid';
}

// closes modal
const closeThemeModal = (e) =>{
    if(e.target.classList.contains('modal-theme')){
        themeModal.style.display = 'none';
    }
}

// open modal
theme.addEventListener('click', openThemeModal);

// close modal
themeModal.addEventListener('click', closeThemeModal);


/* === FONT SIZE === */

const fontSizes = document.querySelectorAll('.choose-size span');
var root = document.querySelector(':root');
const removeSizeSelector = () => {
    fontSizes.forEach(size => {
        size.classList.remove('active');
    })
}

fontSizes.forEach(size => {
    size.addEventListener('click', () => {
        removeSizeSelector();
        let fontSize;
        size.classList.toggle('active');

        if(size.classList.contains('font-size-1')){
            fontSize = '10px';
            root.style.setProperty('----sticky-top-left', '5.4rem');
            root.style.setProperty('----sticky-top-right', '5.4rem');
        } else if(size.classList.contains('font-size-2')){
            fontSize = '13px';
            root.style.setProperty('----sticky-top-left', '5.4rem');
            root.style.setProperty('----sticky-top-right', '-7rem');
        } else if(size.classList.contains('font-size-3')){
            fontSize = '16px';
            root.style.setProperty('----sticky-top-left', '-2rem');
            root.style.setProperty('----sticky-top-right', '-17rem');
        } else if(size.classList.contains('font-size-4')){
            fontSize = '19px';
            root.style.setProperty('----sticky-top-left', '-5rem');
            root.style.setProperty('----sticky-top-right', '-25rem');
        } else if(size.classList.contains('font-size-5')){
            fontSize = '22px';
            root.style.setProperty('----sticky-top-left', '-12rem');
            root.style.setProperty('----sticky-top-right', '-35rem');
        }
    // change font size of the root html element because of rem size
    document.querySelector('html').style.fontSize = fontSize;
    })
})
}


/* === PRIMARY COLOR === */

const colorPalette = document.querySelectorAll('.choose-color span');

// remove active class from colors
const changeActiveColorClass = () => {
    colorPalette.forEach(colorPicker => {
        colorPicker.classList.remove('active');
    })
}

// change primary color
colorPalette.forEach(color => {
    color.addEventListener('click', () => {
        changeActiveColorClass();
        if(color.classList.contains('color-1')){
            primaryHue = 252;
        } else if(color.classList.contains('color-2')){
            primaryHue = 52;
        } else if(color.classList.contains('color-3')){
            primaryHue = 352;
        } else if(color.classList.contains('color-4')){
            primaryHue = 152;
        } else if(color.classList.contains('color-5')){
            primaryHue = 202;
        }
        color.classList.add('active');
        root.style.setProperty('--primary-color-hue', primaryHue);
    })
})

/* === BACKGROUND COLOR === */

const bg1 = document.querySelector('.bg-1');
const bg2 = document.querySelector('.bg-2');
const bg3 = document.querySelector('.bg-3');

let lightColorLightness;
let whiteColorLightness;
let darkColorLightness;

// changes background color
const changeBG = () => {
    root.style.setProperty('--light-color-lightness', lightColorLightness);
    root.style.setProperty('--white-color-lightness', whiteColorLightness);
    root.style.setProperty('--dark-color-lightness', darkColorLightness);
}

bg1.addEventListener('click', () => {
    darkColorLightness = '17%';
    whiteColorLightness = '100%';
    lightColorLightness = '95%';

    // add active class
    bg1.classList.add('active');

    // remove class from others
    bg2.classList.remove('active');
    bg3.classList.remove('active');

    changeBG();
})

bg2.addEventListener('click', () => {
    darkColorLightness = '95%';
    whiteColorLightness = '20%';
    lightColorLightness = '15%';

    // add active class
    bg2.classList.add('active');

    // remove class from others
    bg1.classList.remove('active');
    bg3.classList.remove('active');

    changeBG();
})

bg3.addEventListener('click', () => {
    darkColorLightness = '95%';
    whiteColorLightness = '10%';
    lightColorLightness = '0%';

    // add active class
    bg3.classList.add('active');

    // remove class from others
    bg1.classList.remove('active');
    bg2.classList.remove('active');

    changeBG();
})


/* ==================== PROFIL MODAL ==================== */


/* === MODAL ===*/
if(document.querySelector('#profil') != null){
    // opens modal
    const openProfilModal = () =>{
        profilModal.style.display = 'grid';
    }

    // closes modal
    const closeProfilModal = (e) =>{
        if(e.target.classList.contains('modal-profil')){
            profilModal.style.display = 'none';
        }
    }
    // open modal
    const profilModal = document.querySelector('.modal-profil');
    // close modal
    profilModal.addEventListener('click', closeProfilModal);
    const profil = document.querySelector('#profil');
    profil.addEventListener('click', openProfilModal);
}


/* ==================== ADD FRIEND MODAL ==================== */


/* === MODAL ===*/

if(document.querySelector('#add_friend') != null){
    const addFriend = document.querySelector('#add_friend');
    const addFriendModal = document.querySelector('.modal-add-friend');
    
    // opens modal
    const openAddFriendModal = () =>{
        addFriendModal.style.display = 'grid';
    }
    
    // closes modal
    const closeAddFriendModal = (e) =>{
        if(e.target.classList.contains('modal-add-friend')){
            addFriendModal.style.display = 'none';
        }
    }
    
    // open modal
    addFriend.addEventListener('click', openAddFriendModal);
    
    // close modal
    addFriendModal.addEventListener('click', closeAddFriendModal);
}



/* ==================== ALBUM MODAL ==================== */


/* === MODAL ===*/

// if(document.querySelector('#album') != null){
//     const album = document.querySelector('#album');
//     // opens modal
//     const openAlbumModal = () =>{
//         albumModal.style.display = 'grid';
//     }

//     // open modal
//     album.addEventListener('click', openAlbumModal);
// }

// const albumModal = document.querySelector('.modal-album');

// // closes modal
// const closeAlbumModal = (e) =>{
//     if(e.target.classList.contains('modal-album')){
//         albumModal.style.display = 'none';
//     }
// }

// close modal
// albumModal.addEventListener('click', closeAlbumModal);


/* ==================== CREATE ALBUM MODAL ==================== */


/* === MODAL ===*/

if (document.querySelector('#create_album') != null){
    const createAlbum = document.querySelector('#create_album');
    const createAlbumModal = document.querySelector('.modal-create-album');
    
    // opens modal
    const openCreateAlbumModal = () =>{
        createAlbumModal.style.display = 'grid';
    }
    
    // closes modal
    const closeCreateAlbumModal = (e) =>{
        if(e.target.classList.contains('modal-create-album')){
            createAlbumModal.style.display = 'none';
        }
    }
    
    // open modal
    createAlbum.addEventListener('click', openCreateAlbumModal);
    
    // close modal
    createAlbumModal.addEventListener('click', closeCreateAlbumModal);
}



/* ==================== SETTINGS MODAL ==================== */


/* === MODAL ===*/

if(document.querySelector('#settings') != null){
    const settingsModal = document.querySelector('.modal-settings');

    // opens modal
    const openSettingsModal = () =>{
        settingsModal.style.display = 'grid';
    }

    // closes modal
    const closeSettingsModal = (e) =>{
        if(e.target.classList.contains('modal-settings')){
            settingsModal.style.display = 'none';
        }
    }
    // close modal
    settingsModal.addEventListener('click', closeSettingsModal);
    const settings = document.querySelector('#settings');
    // open modal
    settings.addEventListener('click', openSettingsModal);
}


/* ==================== GROUP MODAL ==================== */


/* === MODAL ===*/
// if(document.querySelector('#group') != null){
//     const group = document.querySelector('#group');
//     // opens modal
//     const openGroupModal = () =>{
//         groupModal.style.display = 'grid';
//     }    
//     // open modal
//     group.addEventListener('click', openGroupModal);
// }

// const groupModal = document.querySelector('.modal-group');

// // closes modal
// const closeGroupModal = (e) =>{
//     if(e.target.classList.contains('modal-group')){
//         groupModal.style.display = 'none';
//     }
// }

// // close modal
// groupModal.addEventListener('click', closeGroupModal);

// function resetUData(){
//     document.getElementById("settings-form").reset();
// }

// function resetUInformations(){
//     document.getElementById("profil-form").reset();
// }

/* ==================== CREATE GROUP MODAL ==================== */


/* === MODAL ===*/

if (document.querySelector('#create_group') != null){
    const createGroup = document.querySelector('#create_group');
    const createGroupModal = document.querySelector('.modal-create-group');
    
    // opens modal
    const openCreateGroupModal = () =>{
        createGroupModal.style.display = 'grid';
    }
    
    // closes modal
    const closeCreateGroupModal = (e) =>{
        if(e.target.classList.contains('modal-create-group')){
            createGroupModal.style.display = 'none';
        }
    }
    
    // open modal
    createGroup.addEventListener('click', openCreateGroupModal);
    
    // close modal
    createGroupModal.addEventListener('click', closeCreateGroupModal);
}



/* ==================== IMAGE MODAL ==================== */


/* === MODAL ===*/

// if(document.querySelector('#image-modify') != null){
//     const image = document.querySelector('#image-modify');
    
//     // opens modal
//     const openImageModal = () =>{
//         imageModal.style.display = 'grid';
//     }

//     // open modal
//     image.addEventListener('click', openImageModal);
    
//     const imageModal = document.querySelector('.modal-image');

//     // closes modal
//     const closeImageModal = (e) =>{
//         if(e.target.classList.contains('modal-image')){
//             imageModal.style.display = 'none';
//         }
//     // close modal
//     imageModal.addEventListener('click', closeImageModal);
//     }
// }




/* ==================== ADD IMAGE MODAL ==================== */


/* === MODAL ===*/

if(document.querySelector('#upload_img') != null){
    const addImage = document.querySelector('#upload_img');
    const addImageModal = document.querySelector('.modal-add-image');
    
    // opens modal
    const openAddImageModal = () =>{
        addImageModal.style.display = 'grid';
    }
    
    // closes modal
    const closeAddImageModal = (e) =>{
        if(e.target.classList.contains('modal-add-image')){
            addImageModal.style.display = 'none';
        }
    }
    
    // open modal
    addImage.addEventListener('click', openAddImageModal);
    
    // close modal
    addImageModal.addEventListener('click', closeAddImageModal);
}
