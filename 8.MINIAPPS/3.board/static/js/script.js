// ── 저장하기 버튼 클릭 ──────────────────
document.querySelector('button').addEventListener('click', function() {
    const title = document.getElementById('input-title').value.trim()
    const contents = document.getElementById('input-text').value.trim()
//추가하기
    if(!title || !contents){
        alert('제목과 내용을 입력해주세요')
        return
    }
    fetch('/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, contents })
    })
    .then(res => res.json())
    .then(data => {
        if (data.result === 'success') {
            document.getElementById('input-title').value = ''
            document.getElementById('input-text').value = ''
            loadList()
        }
    })
})

// ── 목록 불러오기 ────────────────────
function loadList() {
    fetch('/list')
    .then(res => res.json())
    .then(data => {
        const cardList = document.getElementById('card-list')
        cardList.innerHTML = ''

        data.result.forEach(memo => {
            // memo = [id, title, contents, created_at]
            cardList.innerHTML += `
                <div>
                    <h3>${memo[1]}</h3>
                    <p>${memo[2]}</p>
                    <small>${memo[3]}</small>
                    <button onclick="deleteMemo(${memo[0]})">삭제</button>
                </div>
            `
        })
    })
}

//수정하기


//삭제하기
