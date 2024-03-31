let currentmodel = 'ssd300'
let file=0, vfile=0
let timer=0, counter=0
function initmodel() {
    document.getElementById(currentmodel).style.background = '#c57c7c'
    document.getElementById(currentmodel).style.color = 'whitesmoke'
    document.getElementById(currentmodel).innerText+=' - selected'
}
initmodel()
function inputpic(){document.getElementById('inputpic').click();}

document.getElementById('inputpic').onchange = (e)=> {
    document.getElementById('resulttab').style.display='none'
    file=e.target.files[0]
    console.log(file);
    let reader = new FileReader()
    reader.onload = (e)=>{
        document.getElementById('originalimg').setAttribute('src', e.target.result)
        document.getElementById('resultingimg').setAttribute('src', '')
    }
    reader.readAsDataURL(file)
}
document.getElementById('detectOBj').onclick = (e)=>{
    if(file!=0) {
        let formdata = new FormData()
        formdata.append('file', file)
        fetch('http://3.15.4.94:3033/inputpic', {method: 'POST', body: formdata})
            .then((res) => res.json())
            .then((res) => {
                document.getElementById('resultingimg').setAttribute('src', res['link'])
                document.getElementById('resulttab').innerHTML="<label style='color: #c57c7c;'>Results</label>"
                let orig = "<div style=\"color: #c57c7c;\">\n" +
                    "                    <label>Objects found:</label>\n" +
                    "                    <label>" + (res['labels'].length == 0 ? 'No objects detected' : res['labels'].length) + "</label>\n" +
                    "                </div>\n" +
                    "                "
                document.getElementById('resulttab').innerHTML += orig
                let timet = "<div style=\"color: #c57c7c;\">\n" +
                    "                    <label>Time:</label>\n" +
                    "                    <label>" + res['time'] + " secs</label>\n" +
                    "                </div>"
                document.getElementById('resulttab').innerHTML += timet
                for (let i = 0; i < res['labels'].length; i++) {
                    let obj = "<div style=\"color: #c57c7c;\">" +
                        "                    <label>"+(i+1).toString() +") " + res['labels'][i] + ": " + res['scores'][i] + "</label>" +
                        "                </div>"
                    document.getElementById('resulttab').innerHTML += obj
                }
                document.getElementById('resulttab').style.display='flex'
            })
    }
    else window.alert("please select an image")
}

function search(e) {
    let text = document.getElementById('search_box').value
    let url = 'http://3.15.4.94:3033/search?search='+text
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange=()=>{
        if(xhr.status==200 && xhr.readyState==4){
            let res = JSON.parse(xhr.responseText)
            console.log(res);
            displaySearchResults(res['results'])
        }
    }
    xhr.open('GET',url)
    xhr.send()
}

function displaySearchResults(results){
    document.getElementById('images-found').innerText = results[1].length.toString()+' Images found containing '+
        document.getElementById('search_box').value + ' (' + results[0].toString().substring(0,4) +'s)'
    document.getElementById('search-results-frame').innerText=''
    for (let i=0;i<results[1].length;i++) {
        let ele = document.createElement('div')
        let fasd = document.createElement('div')
        fasd.style.zIndex=2
        fasd.style.background='transparent'
        fasd.style.display='none'
        fasd.style.alignContent='center'
        fasd.style.gridArea= '1 / 1'
        let detect=document.createElement('label')
        let download =document.createElement('a')
        detect.innerText='Detect'
        detect.style.background ='whitesmoke'
        detect.style.color ='#c57c7c'
        detect.style.padding='5px'
        detect.style.margin='auto auto'
        detect.id=results[1][i][2]
        detect.style.borderRadius='5px'
        detect.onclick =(e)=>{
            fetch('http://3.15.4.94:3033/detectimg?filename='+e.target.id)
                .then(res=>res.json())
                .then((res)=>{
                    document.getElementById('img-'+e.target.id).src = res['link']
                    console.log(res);
                })
            fasd.style.display='none'
        }
        download.innerText='Download'
        download.style.background ='whitesmoke'
        download.style.color = '#c57c7c'
        download.style.padding='5px'
        download.style.margin='auto auto'
        download.style.textDecoration='none'
        download.href=results[1][i][1]
        download.download = 'File.jpg'
        download.style.borderRadius='5px'
        download.onclick = ()=>{fasd.style.display='none'}
        fasd.append(detect,download)
        fasd.onclick = ()=>{fasd.style.display='none'}
        let img = document.createElement('img')
        img.style.zIndex=1
        img.src = results[1][i][1]
        img.style.objectFit='fill'
        img.style.height='300px'
        img.style.width='300px'
        img.style.gridArea= '1 / 1'
        img.onclick = (e)=>{
            fasd.style.display='flex'
        }
        img.id='img-'+results[1][i][2]
        ele.className='search_result_obj'
        ele.append(img,fasd)
        document.getElementById('search-results-frame').append(ele)
    }
    document.getElementById('detect-frame').style.display='none'
    document.getElementById('videoFinder').style.display='none'
    document.getElementById('search-results').style.display='flex'
    document.getElementById('back').style.visibility='visible'

}

document.getElementById('uploadVideo').onclick= ()=>{
    document.getElementById('videoInputBtn').click()
}
document.getElementById('uploadVideo2').onclick= ()=>{
    document.getElementById('videoInputBtn').click()
}
document.getElementById('videoInputBtn').onchange = (e)=>{
    vfile = e.target.files[0]
    let reader = new FileReader()
    reader.onload = (e)=>{
        document.getElementById('videoPlay').setAttribute('src', e.target.result)
    }
    reader.readAsDataURL(vfile)
    if(vfile!=0){
        console.log(23)
        document.getElementById('parseVideo').style.display='inline'
        document.getElementById('uploadVideo2').style.display='none'
        document.getElementById('hintlbl').style.display='none'
        document.getElementById('videoPlay').style.display='inline'

    }
}
document.getElementById('parseVideo').onclick = ()=>{
    let formdata = new FormData()
    formdata.append('file', vfile)
    document.getElementById('result-area').innerHTML=''
    document.getElementById('objectsfound').innerText = 'Objects found: '
    document.getElementById('parsinglbl').style.display='inline'
    timer = setInterval(()=>{
        document.getElementById('parsinglbl').innerText = 'Parsing'+ '.'.repeat(counter)
        counter+=1
        counter=counter%4
    },600)
    fetch('http://3.15.4.94:3033/inputvid', {method: 'POST', body: formdata})
        .then((res) => res.json())
        .then((res) => {
            clearInterval(timer)
            document.getElementById('parsinglbl').style.display='none'
            let objs=res['objs']
            for(let i=0;i<objs.length;i++){
                let lbl = document.createElement('label')
                lbl.className='result-area-objs'
                lbl.innerText=objs[i]
                document.getElementById('result-area').append(lbl)
            }
            document.getElementById('objectsfound').innerText = 'Objects found: '+objs.length.toString()
            document.getElementById('objectsfound').style.display='inline'
            document.getElementById('result-area').style.display = 'flex'
            document.getElementById('parseVideo').style.display='none'
            document.getElementById('uploadVideo2').style.display='inline'
        })
}

function showVideoFinderWindow(){
    document.getElementById('videoFinder').style.display='flex'
    document.getElementById('search-results').style.display='none'
    document.getElementById('detect-frame').style.display='none'

}

document.getElementById('videotab').onclick = ()=>{
    document.getElementById(currentmodel).style.background='whitesmoke'
    document.getElementById(currentmodel).style.color='black'
    let text = document.getElementById(currentmodel).innerText
    document.getElementById(currentmodel).innerText = text.slice(0,text.indexOf('-'))
    currentmodel='videotab'
    initmodel()
    showVideoFinderWindow()
}
document.getElementById('ssd300').onclick = ()=>{
    document.getElementById('videoFinder').style.display='none'
    document.getElementById('search-results').style.display='none'
    document.getElementById('detect-frame').style.display='flex'
    let text = document.getElementById(currentmodel).innerText
    document.getElementById(currentmodel).innerText = text.slice(0,text.indexOf('-'))
    document.getElementById(currentmodel).style.background='whitesmoke'
    document.getElementById(currentmodel).style.color='black'
    currentmodel='ssd300'
    initmodel()
}

document.getElementById('back').onclick = ()=>{
    document.getElementById('search-results-frame').innerText=''
    document.getElementById('detect-frame').style.display='flex'
    document.getElementById('search-results').style.display='none'
    document.getElementById('back').style.visibility='hidden'
    document.getElementById('search_box').value=''
}

document.getElementById('search_box').onkeydown = (e)=>{
    if(e.key =="Enter"){
        document.getElementById('search').click()
    }
}