import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
  scenarios: {
    normal_users: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '1m', target: 50 }, 
        { duration: '5m', target: 50 }, 
        { duration: '1m', target: 0 }, 
      ],
      gracefulStop: '30s',
      exec: 'normalUser',
    },
    abusive_users: {
      executor: 'constant-vus',
      vus: 10,
      duration: '5m30s',
      exec: 'abusiveUser',
    },
  },
};

const normalUser = () => {
  
  http.get('http://172.21.212.175:30001/category.html');
  sleep(Math.random() * 3); 

  const productIds = ['03fef6ac-1896-4ce8-bd69-b798f85c6e0b', '3395a43e-2d88-40de-b95f-e00e1502085b', '510a0d7e-8e83-4193-b483-e27e09ddc34d', '808a2de1-1aaa-4c25-a9b9-6612e8f29a38', '819e1fbf-8b7e-4f6d-811f-693534916a8b']; 
  const randomProductId = productIds[Math.floor(Math.random() * productIds.length)];
  http.get(`http://172.21.212.175:30001/detail.html?id=${randomProductId}`);
  sleep(Math.random() * 5);

  
  const cartItem = { id: randomProductId};
  const res = http.post('http://172.21.212.175:30001/cart', JSON.stringify(cartItem), { headers: { 'Content-Type': 'application/json' } });
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(Math.random() * 2);

  http.get('http://172.21.212.175:30001/cart');
  sleep(Math.random() * 3);
};

const abusiveUser = () => {
 
  for (let i = 0; i < 10; i++) { 
    http.get('http://172.21.212.175:30001/detail.html?id=819e1fbf-8b7e-4f6d-811f-693534916a8b');
  }
  sleep(Math.random() * 2);

 
  const unauthorizedRes = http.get('http://172.21.212.175:30001/login');
  check(unauthorizedRes, { 'status is 401 or 403': (r) => r.status === 401 || r.status === 403 });
  sleep(Math.random() * 2);

  
  const largePayload = 'x'.repeat(1000000); 
  http.post('http://172.21.212.175:30001/cart', largePayload, { headers: { 'Content-Type': 'application/json' } });
  sleep(Math.random() * 2);
};