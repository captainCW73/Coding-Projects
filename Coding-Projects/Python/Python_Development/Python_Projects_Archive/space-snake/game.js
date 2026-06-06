const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game Constants
const GRID_SIZE = 20;
let TILE_COUNT_X = 0;
let TILE_COUNT_Y = 0;

// Game State
let gameLoop;
let score = 0;
let gems = parseInt(localStorage.getItem('spaceSnakeGems')) || 0;
let isGameOver = false;
let isPaused = false;
let gameSpeed = 100;

// Abilities State
let activeAbility = null;
let abilityTimer = 0;
let abilityCooldown = 0;
const ABILITY_DURATION = 300; // Frames (approx 5-10s depending on speed)
const COOLDOWN_DURATION = 500;

// Snake & Food
let snake = [];
let velocity = { x: 0, y: 0 };
let food = { x: 0, y: 0 };

// Shop Items
const shopItems = [
    {
        id: 'speed',
        name: 'Speed Boost',
        cost: 5,
        icon: '⚡',
        description: 'Move 2x faster for 5s',
        duration: 50 // frames
    },
    {
        id: 'magnet',
        name: 'Magnet',
        cost: 15,
        icon: '🧲',
        description: 'Attract food from distance',
        duration: 150 // frames
    },
    {
        id: 'ghost',
        name: 'Phase Shift',
        cost: 25,
        icon: '👻',
        description: 'Pass through walls & self',
        duration: 100 // frames
    }
];

let inventory = JSON.parse(localStorage.getItem('spaceSnakeInventory')) || {};

// DOM Elements
const scoreDisplay = document.getElementById('score-display');
const gemDisplay = document.getElementById('gem-display');
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over-screen');
const finalScoreSpan = document.getElementById('final-score');
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const shopBtn = document.getElementById('shop-btn');
const shopScreen = document.getElementById('shop-screen');
const closeShopBtn = document.getElementById('close-shop-btn');
const shopGemsDisplay = document.getElementById('shop-gems');
const shopItemsContainer = document.getElementById('shop-items');

// Resize Canvas
function resizeCanvas() {
    canvas.width = window.innerWidth - 40; // Margin
    canvas.height = window.innerHeight - 40;

    // Snap to grid
    canvas.width = Math.floor(canvas.width / GRID_SIZE) * GRID_SIZE;
    canvas.height = Math.floor(canvas.height / GRID_SIZE) * GRID_SIZE;

    TILE_COUNT_X = canvas.width / GRID_SIZE;
    TILE_COUNT_Y = canvas.height / GRID_SIZE;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Input Handling
document.addEventListener('keydown', handleInput);

function handleInput(e) {
    if (isGameOver) return;

    switch (e.key) {
        case 'ArrowUp':
            if (velocity.y === 0) velocity = { x: 0, y: -1 };
            break;
        case 'ArrowDown':
            if (velocity.y === 0) velocity = { x: 0, y: 1 };
            break;
        case 'ArrowLeft':
            if (velocity.x === 0) velocity = { x: -1, y: 0 };
            break;
        case 'ArrowRight':
            if (velocity.x === 0) velocity = { x: 1, y: 0 };
            break;
        case ' ': // Spacebar to activate ability
            activateAbility();
            break;
    }
}

// Shop Logic
function renderShop() {
    shopItemsContainer.innerHTML = '';
    shopGemsDisplay.textContent = gems;

    shopItems.forEach(item => {
        const itemEl = document.createElement('div');
        itemEl.className = 'shop-item';
        const count = inventory[item.id] || 0;

        itemEl.innerHTML = `
            <span class="item-icon">${item.icon}</span>
            <span class="item-name">${item.name}</span>
            <span class="item-desc">${item.description}</span>
            <span class="item-cost">${item.cost} Gems</span>
            <span class="item-count">Owned: ${count}</span>
            <button class="buy-btn neon-btn" onclick="buyItem('${item.id}')">BUY</button>
        `;

        // Add event listener programmatically to avoid scope issues
        const btn = itemEl.querySelector('.buy-btn');
        btn.onclick = () => buyItem(item.id);

        shopItemsContainer.appendChild(itemEl);
    });
}

function buyItem(itemId) {
    const item = shopItems.find(i => i.id === itemId);
    if (gems >= item.cost) {
        gems -= item.cost;
        inventory[itemId] = (inventory[itemId] || 0) + 1;

        // Save
        localStorage.setItem('spaceSnakeGems', gems);
        localStorage.setItem('spaceSnakeInventory', JSON.stringify(inventory));

        // Update UI
        gemDisplay.textContent = gems;
        renderShop();
    } else {
        alert("Not enough gems!");
    }
}

function toggleShop() {
    if (shopScreen.classList.contains('hidden')) {
        shopScreen.classList.remove('hidden');
        renderShop();
    } else {
        shopScreen.classList.add('hidden');
    }
}

// Ability Logic
function activateAbility() {
    if (activeAbility) return; // Already active

    // Check for available abilities in order of priority or selection
    // For simplicity, we'll activate the first available one or cycle
    // Let's implement a simple priority: Ghost > Magnet > Speed

    let abilityToUse = null;
    if (inventory['ghost'] > 0) abilityToUse = 'ghost';
    else if (inventory['magnet'] > 0) abilityToUse = 'magnet';
    else if (inventory['speed'] > 0) abilityToUse = 'speed';

    if (abilityToUse) {
        inventory[abilityToUse]--;
        localStorage.setItem('spaceSnakeInventory', JSON.stringify(inventory));

        activeAbility = abilityToUse;
        const item = shopItems.find(i => i.id === abilityToUse);
        abilityTimer = item.duration;

        // Visual feedback
        console.log(`Activated ${abilityToUse}`);
    }
}

// Game Logic
function initGame() {
    snake = [
        { x: 10, y: 10 },
        { x: 9, y: 10 },
        { x: 8, y: 10 }
    ];
    velocity = { x: 1, y: 0 };
    score = 0;
    isGameOver = false;
    activeAbility = null;
    abilityTimer = 0;

    scoreDisplay.textContent = score;
    gemDisplay.textContent = gems;

    spawnFood();

    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    shopScreen.classList.add('hidden');

    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(update, 100); // 10 FPS base
}

function spawnFood() {
    food = {
        x: Math.floor(Math.random() * TILE_COUNT_X),
        y: Math.floor(Math.random() * TILE_COUNT_Y)
    };
    // Check collision with snake
    for (let part of snake) {
        if (part.x === food.x && part.y === food.y) {
            spawnFood();
            break;
        }
    }
}

function update() {
    if (isGameOver || isPaused) return;

    // Ability Timer
    if (activeAbility) {
        abilityTimer--;
        if (abilityTimer <= 0) {
            activeAbility = null;
        }
    }

    // Speed Boost Logic (Move twice per frame if active)
    let steps = (activeAbility === 'speed') ? 2 : 1;

    for (let i = 0; i < steps; i++) {
        moveSnake();
        if (isGameOver) return;
    }

    draw();
}

function moveSnake() {
    const head = { x: snake[0].x + velocity.x, y: snake[0].y + velocity.y };

    // Magnet Ability Logic
    if (activeAbility === 'magnet') {
        // Simple magnet: if food is within 5 tiles, move it one step closer
        const dist = Math.abs(head.x - food.x) + Math.abs(head.y - food.y);
        if (dist < 8 && dist > 0) {
            if (food.x < head.x) food.x++;
            else if (food.x > head.x) food.x--;

            if (food.y < head.y) food.y++;
            else if (food.y > head.y) food.y--;
        }
    }

    // Wall Collision
    if (head.x < 0 || head.x >= TILE_COUNT_X || head.y < 0 || head.y >= TILE_COUNT_Y) {
        if (activeAbility === 'ghost') {
            // Wrap around
            if (head.x < 0) head.x = TILE_COUNT_X - 1;
            if (head.x >= TILE_COUNT_X) head.x = 0;
            if (head.y < 0) head.y = TILE_COUNT_Y - 1;
            if (head.y >= TILE_COUNT_Y) head.y = 0;
        } else {
            gameOver();
            return;
        }
    }

    // Self Collision
    for (let part of snake) {
        if (head.x === part.x && head.y === part.y) {
            if (activeAbility !== 'ghost') {
                gameOver();
                return;
            }
        }
    }

    snake.unshift(head);

    // Eat Food
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        gems += 1;
        localStorage.setItem('spaceSnakeGems', gems);
        scoreDisplay.textContent = score;
        gemDisplay.textContent = gems;
        spawnFood();
    } else {
        snake.pop();
    }
}

function draw() {
    // Clear
    ctx.fillStyle = '#050510'; // Match CSS bg
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw Food
    ctx.fillStyle = '#ff00ff'; // Secondary Neon
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#ff00ff';
    ctx.beginPath();
    ctx.arc(
        food.x * GRID_SIZE + GRID_SIZE / 2,
        food.y * GRID_SIZE + GRID_SIZE / 2,
        GRID_SIZE / 2 - 2,
        0, Math.PI * 2
    );
    ctx.fill();
    ctx.shadowBlur = 0;

    // Draw Snake
    snake.forEach((part, index) => {
        // Color based on ability
        if (activeAbility === 'speed') ctx.fillStyle = '#ffff00';
        else if (activeAbility === 'magnet') ctx.fillStyle = '#ff0000';
        else if (activeAbility === 'ghost') ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        else ctx.fillStyle = '#00f3ff';

        // Head glow
        if (index === 0) {
            ctx.shadowBlur = 20;
            ctx.shadowColor = ctx.fillStyle;
        } else {
            ctx.shadowBlur = 0;
        }

        ctx.fillRect(
            part.x * GRID_SIZE + 1,
            part.y * GRID_SIZE + 1,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        );
    });
    ctx.shadowBlur = 0;

    // Draw Ability Indicator
    if (activeAbility) {
        ctx.fillStyle = '#fff';
        ctx.font = '20px Outfit';
        ctx.fillText(`ABILITY: ${activeAbility.toUpperCase()} (${abilityTimer})`, 20, canvas.height - 20);
    }
}

function gameOver() {
    isGameOver = true;
    clearInterval(gameLoop);
    finalScoreSpan.textContent = score;
    gameOverScreen.classList.remove('hidden');
}

// Event Listeners
startBtn.addEventListener('click', initGame);
restartBtn.addEventListener('click', initGame);
shopBtn.addEventListener('click', toggleShop);
closeShopBtn.addEventListener('click', toggleShop);

// Initial Render
resizeCanvas();
gemDisplay.textContent = gems;
