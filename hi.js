const cells = document.querySelectorAll('.cell');
const status = document.getElementById('status');
const restartBtn = document.getElementById('restart-btn');

let board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
];

let currentPlayer = 1; // 1 for 'X', 2 for 'O'
let gameOver = false;

const checkWin = (player) => {
    // Check rows, columns, and diagonals for a win
    for (let i = 0; i < 3; i++) {
        if (board[i][0] === player && board[i][1] === player && board[i][2] === player) return true; // Check row
        if (board[0][i] === player && board[1][i] === player && board[2][i] === player) return true; // Check column
    }
    if (board[0][0] === player && board[1][1] === player && board[2][2] === player) return true; // Check diagonal
    if (board[0][2] === player && board[1][1] === player && board[2][0] === player) return true; // Check reverse diagonal
    return false;
};

const isBoardFull = () => {
    for (let row of board) {
        if (row.includes(0)) return false;
    }
    return true;
};

const handleCellClick = (e) => {
    if (gameOver) return;
    const row = e.target.dataset.row;
    const col = e.target.dataset.col;

    if (board[row][col] === 0) {
        board[row][col] = currentPlayer;
        e.target.textContent = currentPlayer === 1 ? 'X' : 'O';

        if (checkWin(currentPlayer)) {
            status.textContent = currentPlayer === 1 ? "Player Wins!" : "Computer Wins!";
            gameOver = true;
        } else if (isBoardFull()) {
            status.textContent = "It's a Draw!";
            gameOver = true;
        } else {
            currentPlayer = currentPlayer === 1 ? 2 : 1; // Switch turn
            status.textContent = currentPlayer === 1 ? "Player's Turn" : "Computer's Turn";
        }
    }
};

const restartGame = () => {
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ];
    gameOver = false;
    currentPlayer = 1;
    status.textContent = "Player's Turn";
    cells.forEach(cell => cell.textContent = '');
};

cells.forEach(cell => cell.addEventListener('click', handleCellClick));
restartBtn.addEventListener('click', restartGame);
