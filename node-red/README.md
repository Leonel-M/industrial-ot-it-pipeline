# Node-RED Flow — Dashboard HMI Móvil

## Requisitos
npm install node-red-contrib-opcua@0.2.354 node-red-dashboard@3.6.6 node-red-contrib-ui-led@0.4.11

## Importar
1. Abre Node-RED (http://localhost:1880)
2. Menú (☰) → Import → selecciona flows.json
3. Abre el nodo "CODESYS SUBSCRIBE" o "CODESYS WRITE" → edita el Endpoint 
   "CODESYS-LAMS" con tu propio host y credenciales (usuario/contraseña 
   no se exportan por seguridad)
4. Deploy
5. Accede al dashboard en http://localhost:1880/ui

## Arquitectura
- Bloque READ: 4 inject (uno por variable) → OpcUa-Client (subscribe) → 
  rbe (filtra sin cambios) / switch (demux por topic) → widgets UI
- Bloque WRITE: ui_button/ui_slider → trigger (pulso 250ms) → OpcUa-Item → 
  OpcUa-Client (write)