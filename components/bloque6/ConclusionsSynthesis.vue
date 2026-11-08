<template>
  <div class="syn-wrap">
    <div class="syn-questions">
      <article class="syn-card syn-card--cyan">
        <span class="syn-num">01</span>
        <h3>¿Qué reglas debemos proteger?</h3>
        <p>
          Cuando una entidad posee <strong>invariantes de dominio</strong> que nunca deben quebrarse, el encapsulamiento y los contratos de clase centralizan su integridad.
        </p>
      </article>

      <article class="syn-card syn-card--indigo">
        <span class="syn-num">02</span>
        <h3>¿Qué partes van a cambiar?</h3>
        <p>
          Cuando el negocio exige intercambiar tarifas, pasarelas o algoritmos sin tocar el núcleo, el <strong>polimorfismo, la composición y Strategy</strong> evitan condicionales frágiles.
        </p>
      </article>

      <article class="syn-card syn-card--emerald">
        <span class="syn-num">03</span>
        <h3>¿Cuál es el costo dominante?</h3>
        <p>
          En dominios complejos mantenidos en equipo, la claridad modular de POO compensa su estructura; en scripts breves o cómputo matricial, un enfoque procedural o funcional suele ser más directo.
        </p>
      </article>
    </div>

    <div class="syn-banner">
      <p class="syn-banner__p">
        <strong>Síntesis Multiparadigma en Ingeniería Moderna:</strong>
        POO organiza las fronteras entre módulos y contratos (nivel macro), el estilo funcional aporta transformaciones puras e inmutables dentro de los métodos (nivel micro) y el estilo imperativo expresa algoritmos secuenciales claros.
      </p>
    </div>
  </div>
</template>

<style scoped>
.syn-wrap {
  flex: 1;
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  gap: 0.7rem;
  min-width: 0;
  min-height: 0;
}

.syn-questions {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.syn-card {
  box-sizing: border-box;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1rem 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.syn-card--cyan {
  border-top: 3px solid var(--accent-interface);
}

.syn-card--indigo {
  border-top: 3px solid var(--accent-class);
}

.syn-card--emerald {
  border-top: 3px solid var(--accent-valid);
}

.syn-num {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 800;
  color: #7dd3fc;
}

.syn-card h3 {
  font-size: 1.02rem;
  line-height: 1.25;
  font-weight: 700;
}

.syn-card p {
  font-size: 0.8rem;
  line-height: 1.46;
  color: var(--text-secondary);
}

.syn-banner {
  background: rgba(56, 189, 248, 0.09);
  border: 1px solid rgba(56, 189, 248, 0.36);
  border-radius: var(--radius-md);
  padding: 0.72rem 1rem;
}

.syn-banner__p {
  font-size: 0.8rem;
  line-height: 1.45;
  color: var(--text-secondary);
}

.syn-banner strong {
  color: var(--text-primary);
  margin-right: 0.35rem;
}
</style>
