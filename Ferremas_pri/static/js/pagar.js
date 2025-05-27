function pagar() {
  const payload = {
    commerceId: "mi_commerce_id",
    commercePaymentId: "mi_commerce_payment_id",
    processorPaymentId: "mi_processor_payment_id",
    serviceId: "mi_service_id",
    clientId: "mi_client_id"
  };

  fetch('/realizar_pago/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    console.log('Respuesta Transbank:', data);
    alert('Pago procesado: ' + (data.status || 'Sin status'));
  });
}
