const $ = (sel) => document.querySelector(sel)
const $$ = (sel) => document.querySelectorAll(sel)

showDowloadedVideos()

$('[btn]').addEventListener('click', (x)=>{
    
    $('[info]>p').innerText = ''
    x.target.innerText = 'Downloading...'

    fetch(`/api/download-video?url=${$('[inp]').value}`).then(
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

    fetch(`/api/all-downloaded`).then(
        data => data.json()
    ).then(response => {
        if(response.status == "ok"){
            $('[video-holder]').innerHTML = ``
            response.videos.map(video=>{
                $('[video-holder]').innerHTML +=  `

                <div video id="${video[0]}">
                   <p hidden videoPath=${video[5]}></p>
                   <h4 credit>by <a target="_blank" href="https://www.tiktok.com/@${video[1]}">${video[1]}</a></h4>
                   <h5 tags>${video[4]}</h5>
                   <img cover src="${video[3]}">
                   <div actions>
                    <button onclick=showYoutubeModal("${video[0]}") upload>Upload to Youtube</button> <button onclick=removeVideo(${video[0]}) remove>Remove Video</button>
                   </div>
                <div>
                `
            })
        } else {
            $('[video-holder]').innerText = 'Here is no video downloaded, download some!'
        }
    })

}

function changeBackGroundBlur(){

    $('[container]').classList.value == 'blur' ?
    ($('[container]').classList.remove('blur'), closeModal()) : $('[container]').classList.add('blur')

}

function closeModal(){

    $('[yt-modal]') != null ? $('[yt-modal]').remove() : ''  

}

function showYoutubeModal(id){
    const description = $$(`[id='${id}']>[tags]`)[0].textContent || ''
    const credit = $$(`[id='${id}']>[credit]`)[0].textContent || ''

    changeBackGroundBlur()

    modal_style = `
        height: 350px;
        width: 500px;
        position: fixed;
        top: 50%;
        right: 50%;
        transform: translate(50%,-50%);
        background: white;
        color: black;
    `
    head_style = `
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #dddddd;
    `
    close_style = `
       color: red;
       cursor: pointer;
    `
    modal_body_style = `
        padding: 10px;
    `
    title_style = `
        width: 96%;
        padding: 5px;
    `
    description_style = `
        max-height: 65px;
        width: 470px;
        padding: 5px;
        max-width: 96%;
        margin: 0px;
        height: 74px;
    `
    tags_container_style = `
        display: flex;
        justify-content: space-between;
        align-content: space-between;
    `
    gen_tags_style = `
        cursor: pointer;
        margin-right: 6px;
        background: #115dbc;
        color: white;
        border: 0px;
        padding: 3px;
    `
    close_mouseOver_style = `
        this.style.transform = 'rotate(180deg)';
    `
    close_mouseOut_style = `
        this.style.transform = 'rotate(0deg)';
    `
    tags_style = title_style
    final_upload_style = `
        cursor: pointer;
        width: 30%;
        height: 33px;
        background: #ff0000;
        border: 1px solid black;
        border-radius: 3px;
        color: white;
        margin-top: 10px;
        font-size: 12px;
    `
    final_upload_mouseOver_style = `
        this.style.fontSize = '13px';
    `
    final_upload_mouseOut_style = `
        this.style.fontSize = '12px';
    `

    html = `
        <div style="${modal_style}" yt-modal>
            <div style="${head_style}" modal-head>
                <h4>YouTube Uploader</h4>
                <h2 style="${close_style}" onclick=changeBackGroundBlur() onmouseover="${close_mouseOver_style}" onmouseout="${close_mouseOut_style}">???</h2>
            </div>
            <div style="${modal_body_style}" modal-body>
                <h4>Video Title</h4>
                <input style="${title_style}" title placeholder="Me at the zoo" type="text"/>
                <h4>Description</h4>
                <textarea style="${description_style}" description placeholder="hello world">${description}\n\n${credit}</textarea>
                <div style="${tags_container_style}" tags-container>
                    <h4>tags</h4><button style="${gen_tags_style}" onclick=generateTags() gen-tags>Generate Tags</button>
                </div>
                <input style="${tags_style}" tags placeholder="#tag1 #tag2" type="text"/>
                <button style="${final_upload_style}" onmouseover="${final_upload_mouseOver_style}" onmouseout="${final_upload_mouseOut_style}" onclick=upload(${id}) final-upload>Upload Video ???</button>
            </div>
        </div>
    `
    if($('[yt-modal]') == null){
        $('[modal-container]').innerHTML += html
    }

}

function removeVideo(id){

    $$(`[id='${id}']>div>button`)[1].innerText = 'Removing...'
    
    fetch(`/api/remove-video?id=${id}`).then(
        data => data.json()
    ).then(response => {
        if(response.status == "ok"){
            showDowloadedVideos()
        } 
    })

}

function generateTags(){
    
    var inputTagVal = $('input[tags]').value

    if(inputTagVal.length > 0 && inputTagVal.replaceAll(' ', '').length > 0){
        $('[gen-tags]').innerText = 'Generating Tags...'
        fetch(`/api/tags-suggestions?query=${inputTagVal}`).then(
            data => data.json()
        ).then(response => {
            if(response.status == "ok"){
                var inp = ''
                response.tags.map((tag)=>{
                    inp += tag + ','
                })

                $('input[tags]').value = inp.slice(0, -1)
                $('[gen-tags]').innerText = 'Generate Tags'
            } else {
                $('[gen-tags]').innerText = 'Generate Tags'
            }
        })
    }
    
}

function upload(id){
    const videoPath = $$(`[id='${id}']>[videoPath]`)[0].getAttribute('videoPath')
    const title = $('[modal-body]>[title]').value || 'title'
    const description = $('[modal-body]>[description]').value || ''
    const keywords = $('[modal-body]>[tags]').value || ''
    
    alert("Go and make the google authorization through CLI")

    changeBackGroundBlur()

    fetch(`/api/upload-video?file=${videoPath}&title=${title}&description=${description}&keywords=${keywords}`)
}