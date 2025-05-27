document.addEventListener('DOMContentLoaded', function() {
  const pagarBtn = document.getElementById("pagar-btn");
  const cargandoDiv = document.getElementById("cargando");

  if (!pagarBtn) {
    console.warn("Botón 'pagar-btn' no encontrado");
    return;
  }

  function pagar() {
    const totalElement = document.getElementById("total-compra");
    if (!totalElement) {
      alert("No se encontró el elemento con id 'total-compra'");
      return;
    }

    const total = totalElement.innerText.trim();

    const payload = {
      commerceId: "mi_commerce_id",
      commercePaymentId: "orden_" + Date.now(),
      processorPaymentId: "proc_" + Date.now(),
      serviceId: "mi_service_id",
      clientId: "cliente_123",
      total: total,
    };

    pagarBtn.disabled = true;
    cargandoDiv.style.display = "block";

    fetch('/realizar_pago/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(res => {
      if (!res.ok) throw new Error('Error HTTP ' + res.status);
      return res.json();
    })
    .then(data => {
      console.log('Respuesta Transbank:', data);
      alert('Pago procesado: ' + (data.status || 'Sin status'));
    })
    .catch(err => {
      alert('Error en el pago: ' + err.message);
      console.error(err);
    })
    .finally(() => {
      pagarBtn.disabled = false;
      cargandoDiv.style.display = "none";
    });
  }

  pagarBtn.addEventListener('click', pagar);
});
