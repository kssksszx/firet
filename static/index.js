document.addEventListener('DOMContentLoaded', function () {
    const gameBoard = document.getElementById('game-board');
    const gameResult = document.getElementById('game-result');
    const resetBtn = document.getElementById('reset-btn');

    resetBtn.addEventListener('click', resetGame);

    function resetGame() {
        fetch('/make_move', { method: 'POST', body: new URLSearchParams('column=0') })
            .then(response => response.json())
            .then(data => {
                updateBoard(data.board);
                gameResult.innerText = '';
            });
    }

    gameBoard.addEventListener('click', function (event) {
        if (event.target.tagName === 'TD') {
            const column = event.target.cellIndex;
            makeMove(column);
        }
    });

    function makeMove(column) {
        fetch('/make_move', { method: 'POST', body: new URLSearchParams('column=' + column) })
            .then(response => response.json())
            .then(data => {
                updateBoard(data.board);
                if (data.result === 1) {
                    gameResult.innerText = 'You win!';
                } else if (data.result === -1) {
                    gameResult.innerText = 'AI wins!';
                } else if (data.result === 0 && data.player_turn === 'X') {
                    gameResult.innerText = "It's a draw!";
                }
            });
    }

    function updateBoard(board) {
        for (let i = 0; i < gameBoard.rows.length; i++) {
            for (let j = 0; j < gameBoard.rows[i].cells.length; j++) {
                gameBoard.rows[i].cells[j].innerText = board[i][j];
            }
        }
    }
});
