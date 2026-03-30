<script>
	let { map = [] } = $props();
</script>

<div class="glass-card rhythm-container">
	<h3 style="color: var(--text-muted); margin-bottom: 1.5rem; text-align: center;">Visual Rhythm Map</h3>

	<div class="map-layout">
		{#each map as line, lineIndex}
			<div class="rhythm-line">
				{#each line as word, wordIndex}
					<div class="rhythm-word" style="display: flex; flex-direction: column; align-items: center; gap: 0.25rem;">
						<div class="syllables-container" style="display: flex; flex-direction: row; gap: 2px;">
							{#each word as syllable}
								<div class={`syllable-block weight-${syllable.weight}`}>
									<span class="devanagari">{syllable.char}</span>
									<span class="weight-label">{syllable.weight}</span>
								</div>
							{/each}
						</div>
						
						<!-- Calculate total word weight -->
						<div class="word-total" style="color: var(--text-muted); font-weight: 600; font-size: 0.95rem; line-height: 1; margin-top: 0.2rem;">
							({word.reduce(/** @param {number} sum */ /** @param {{weight: number}} s */ (sum, s) => sum + s.weight, 0)})
						</div>
					</div>
				{/each}
			</div>
		{/each}
	</div>
</div>

<style>
	.rhythm-container {
		background: rgba(0, 0, 0, 0.4);
	}

	.map-layout {
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.rhythm-line {
		display: flex;
		flex-wrap: nowrap;
		gap: 1rem;
		justify-content: flex-start;
		overflow-x: auto;
		padding-bottom: 1rem;
	}

	.rhythm-word {
		background: rgba(255, 255, 255, 0.03);
		padding: 0.5rem 0.5rem 0.25rem 0.5rem;
		border-radius: 8px;
		border: 1px solid var(--glass-border);
	}

	.syllable-block {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
		padding: 0.5rem 0 0 0;
		width: 48px;
		height: 70px;
		border-radius: 6px;
		color: #1e293b;
		transition: transform 0.2s ease, filter 0.2s ease;
		cursor: default;
	}
	.syllable-block:hover {
		transform: translateY(-2px);
		filter: brightness(1.05);
	}

	.weight-1 {
		background: #fdba74; /* Pastel Orange */
		box-shadow: 0 4px 12px rgba(253, 186, 116, 0.15);
	}

	.weight-2 {
		background: #93c5fd; /* Pastel Blue */
		box-shadow: 0 4px 12px rgba(147, 197, 253, 0.15);
		width: 58px;
	}

	.syllable-block .devanagari {
		font-size: 1.8rem;
		line-height: 1;
		margin-top: 0.2rem;
	}

	.weight-label {
		font-family: var(--font-sans);
		font-size: 0.85rem;
		font-weight: 800;
		opacity: 0.9;
		color: var(--text-main);
		border-top: 1px solid rgba(0, 0, 0, 0.1);
		width: 100%;
		text-align: center;
		padding: 0.15rem 0;
		background: rgba(0, 0, 0, 0.04);
	}

	.word-total {
		margin-left: 0.5rem;
		color: var(--text-muted);
		font-weight: 600;
		font-size: 1rem;
	}
</style>
