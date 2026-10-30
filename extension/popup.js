// Tab Switching
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).classList.add('active');
  });
});

// Gas Calculator
function setGwei(val) {
  document.getElementById('gas-gwei').value = val;
  calcGas();
}

function calcGas() {
  const gwei = parseFloat(document.getElementById('gas-gwei').value) || 0;
  const eth = parseFloat(document.getElementById('gas-eth').value) || 0;
  const cost = (units) => '$' + (units * gwei * 1e-9 * eth).toFixed(2);
  document.getElementById('cost-transfer').textContent = cost(21000);
  document.getElementById('cost-erc20').textContent = cost(65000);
  document.getElementById('cost-swap').textContent = cost(150000);
}
document.getElementById('gas-gwei').addEventListener('input', calcGas);
document.getElementById('gas-eth').addEventListener('input', calcGas);

// Impermanent Loss Calculator
function calcIL() {
  const deposit = parseFloat(document.getElementById('il-deposit').value) || 0;
  const changePct = parseFloat(document.getElementById('il-ratio').value) || 0;
  const r = 1 + (changePct / 100);
  let il = 0;
  if (r > 0) il = (2 * Math.sqrt(r)) / (1 + r) - 1;
  const ilPct = il * 100;
  const hodlVal = deposit * 0.5 + deposit * 0.5 * r;
  const poolVal = hodlVal * (1 + il);
  const lossUsd = hodlVal - poolVal;

  document.getElementById('res-il-pct').textContent = ilPct.toFixed(2) + '%';
  document.getElementById('res-il-usd').textContent = '-$' + Math.abs(lossUsd).toFixed(2);
  document.getElementById('res-pool-val').textContent = '$' + poolVal.toFixed(2);
  document.getElementById('res-hodl-val').textContent = '$' + hodlVal.toFixed(2);
}
document.getElementById('il-deposit').addEventListener('input', calcIL);
document.getElementById('il-ratio').addEventListener('input', calcIL);

// Profit Calculator
function calcProfit() {
  const buy = parseFloat(document.getElementById('p-buy').value) || 0;
  const sell = parseFloat(document.getElementById('p-sell').value) || 0;
  const qty = parseFloat(document.getElementById('p-qty').value) || 0;
  const feeRate = (parseFloat(document.getElementById('p-fee').value) || 0) / 100;

  const totalBuy = buy * qty;
  const totalSell = sell * qty;
  const entryFee = totalBuy * feeRate;
  const exitFee = totalSell * feeRate;
  const totalFees = entryFee + exitFee;
  const netProfit = (totalSell - totalBuy) - totalFees;
  const roi = totalBuy > 0 ? (netProfit / totalBuy) * 100 : 0;

  document.getElementById('res-p-net').textContent = (netProfit >= 0 ? '+$' : '-$') + Math.abs(netProfit).toFixed(2);
  document.getElementById('res-p-roi').textContent = (roi >= 0 ? '+' : '') + roi.toFixed(2) + '%';
  document.getElementById('res-p-fees').textContent = '$' + totalFees.toFixed(2);
}
document.getElementById('p-buy').addEventListener('input', calcProfit);
document.getElementById('p-sell').addEventListener('input', calcProfit);
document.getElementById('p-qty').addEventListener('input', calcProfit);
document.getElementById('p-fee').addEventListener('input', calcProfit);

calcGas();
calcIL();
calcProfit();
