const $ = (sel) => document.querySelector(sel)
const $$ = (sel) => document.querySelectorAll(sel)

const apiUrl = `${window.location.protocol}//${window.location.host}`

showDowloadedVideos()

$('[btn]').addEventListener('click', (x)=>{
    
    $('[info]>p').innerText = ''
    x.target.innerText = 'Downloading...'

    fetch(`${apiUrl}/api/download-video?url=${$('[inp]').value}`).then(
        data => data.json()
    ).then(response => {
        x.target.innerText = 'Download'
        $('[info]>p').innerText = response.message
        setTimeout(() => {
            $('[info]>p').innerText = ``
        }, 5000)
        $('[inp]').value = ''
        showDowloadedVideos()
        if(response.status == "ok"){
            $('[info]>p').style.color = 'green'
        } else {
            $('[info]>p').style.color = 'red'
        }
    })

})


function showDowloadedVideos(){

    fetch(`${apiUrl}/api/all-downloaded`).then(
        data => data.json()
    ).then(response => {
        if(response.status == "ok"){
            $('[video-holder]').innerHTML = ``
            response.videos.map(video=>{
                $('[video-holder]').innerHTML +=  `

                <div video id="${video[0]}">
                   <h4>by <a target="_blank" href="https://www.tiktok.com/@${video[1]}">${video[1]}</a></h4>
                   <h5>${video[4]}</h5>
                   <img cover src="${video[3]}">
                   <div actions>
                    <button upload>Upload to Youtube</button> <button onclick=removeVideo(${video[0]}) remove>Remove from DB</button>
                   </div>
                <div>
                `
            })
        } else {
            $('[video-holder]').innerText = 'Here is no video downloaded, download some!'
        }
    })

}

function removeVideo(id){

    $$(`[id='${id}']>div>button`)[1].innerText = 'Removing...'
    
    fetch(`${apiUrl}/api/remove-video?id=${id}`).then(
        data => data.json()
    ).then(response => {
        if(response.status == "ok"){
            showDowloadedVideos()
        } 
    })

}