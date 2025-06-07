export async function runMonitoring(params) {
  console.log("Mock request with:", params);
  await new Promise((r) => setTimeout(r, 500)); // задержка
  return {
    count: 37,
    median: 120000,
    min: 80000,
    max: 200000
  };
}
