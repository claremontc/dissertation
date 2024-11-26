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

const generateRandomUsername = () => {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let username = '';
  for (let i = 0; i < 8; i++) {
    username += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return username;
};

const productIds = ['03fef6ac-1896-4ce8-bd69-b798f85c6e0b', '3395a43e-2d88-40de-b95f-e00e1502085b', '510a0d7e-8e83-4193-b483-e27e09ddc34d', '808a2de1-1aaa-4c25-a9b9-6612e8f29a38', '819e1fbf-8b7e-4f6d-811f-693534916a8b'];

export function normalUser() {
    http.get('http://172.21.212.175:30001/category.html');
    sleep(Math.random() * 3); 
  
    const randomProductId = productIds[Math.floor(Math.random() * productIds.length)];
    http.get(`http://172.21.212.175:30001/detail.html?id=${randomProductId}`);
    sleep(Math.random() * 5);
  
    const cartItem = { id: randomProductId};
    const res = http.post('http://172.21.212.175:30001/cart', JSON.stringify(cartItem), { headers: { 'Content-Type': 'application/json' } });
    check(res, { 'status is 201': (r) => r.status === 201 });
    sleep(Math.random() * 2);
  
    http.get('http://172.21.212.175:30001/cart');
    sleep(Math.random() * 3);
 
    const searchTerm = 'brown'; 
    http.get(`http://172.21.212.175:30001/category.html?tags=${searchTerm}`);
    sleep(Math.random() * 3);

    http.get('http://172.21.212.175:30001/customer-orders.html');
    sleep(Math.random() * 3);
  
    http.get('http://172.21.212.175:30001/customers/jn5Lxykw_jVwNS8XDaMs4l85jd0NmMK8');
    sleep(Math.random() * 2);
    
    //http.get('http://172.21.212.175:30001/orders');
    //sleep(Math.random() * 3);

    const username = generateRandomUsername();
    //console.log(username);
    const userId = Math.floor(Math.random() * 50);
    const userData = { username: username, password: "Test@123", email: `celestinaclaremont497${userId}@gmail.com`, firstName: "Celestina", lastName: "Claremont" };
    //console.log(userData);
    const resp = http.post('http://172.21.212.175:30001/register', JSON.stringify(userData), { headers: { 'Content-Type': 'application/json' } });
   // console.log(resp);
    check(resp, { 'status is 200': (r) => r.status === 200 });
    sleep(Math.random() * 2);
}

export function abusiveUser() {
  for (let i = 0; i < 20; i++) { 
    http.get(`http://172.21.212.175:30001/detail.html?id=${productIds[Math.floor(Math.random() * productIds.length)]}`);
  }
  sleep(Math.random() * 2);

  const unauthorizedRes = http.get('http://172.21.212.175:30001/login'); 
  check(unauthorizedRes, { 'status is 401 or 403': (r) => r.status === 401 || r.status === 403 });
  sleep(Math.random() * 2);

  const tamperedProductId = 'invalid-product-id';
  http.get(`http://172.21.212.175:30001/detail.html?id=${tamperedProductId}`);
  sleep(Math.random() * 2);

  const largePayload = 'x'.repeat(5000000); 
  http.post('http://172.21.212.175:30001/cart', largePayload, { headers: { 'Content-Type': 'application/json' } });
  sleep(Math.random() * 2);

  const stolenCookie = 'jn5Lxykw_jVwNS8XDaMs4l85jd0NmMK8';
  http.get('http://172.21.212.175:30001/orders', { headers: { 'logged_in': stolenCookie } });
  sleep(Math.random() * 2);

  for (let i = 0; i < 100; i++) {
    http.get('http://172.21.212.175:30001/cart');
  }
  sleep(Math.random() * 2);

  const xssPayload = '<script>alert("XSS")</script>';
  http.post('http://172.21.212.175:30001/cart', xssPayload, { headers: { 'Content-Type': 'application/json' } });
  sleep(Math.random() * 2);
}