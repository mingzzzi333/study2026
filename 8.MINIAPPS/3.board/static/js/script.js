// ── 저장하기 버튼 클릭 ──────────────────
document.querySelector('button').addEventListener('click', function() {
    const title = document.getElementById('input-title').value.trim()
    const contents = document.getElementById('input-text').value.trim()
