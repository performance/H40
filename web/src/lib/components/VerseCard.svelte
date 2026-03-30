<script>
	let { verse } = $props();

	let showDictionary = $state(true);
</script>

<div class="glass-card card-container">
	<!-- Awadhi Text -->
	<div class="text-block main-script">
		<div class="devanagari script-line">{verse.text.awadhi}</div>
		<div class="telugu script-line">{verse.text.telugu}</div>
		<div class="iast script-line">{verse.text.iast}</div>
	</div>

	<hr class="divider" />

	<!-- Translations -->
	<div class="text-block translation-block">
		{#if verse.translation.sanskrit && verse.translation.sanskrit.length > 0}
			<div class="sanskrit-meaning" style="font-family: var(--font-deva); margin-bottom: 0.75rem; color: var(--text-main);">
				<strong>सरल-संस्कृतम्:</strong>
				{#each verse.translation.sanskrit as sLine}
					<div>{sLine}</div>
				{/each}
			</div>
		{/if}
		{#if verse.translation.english && verse.translation.english.length > 0}
			<div class="english-meaning">
				{#each verse.translation.english as eLine}
					<div>{eLine}</div>
				{/each}
			</div>
		{/if}
	</div>

	<!-- Dictionary Toggle — hidden for Dohas which have no word table -->
	{#if verse.type !== 'doha' && verse.word_meanings && verse.word_meanings.length > 0}
		<div class="dictionary-section">
			<button class="dict-toggle" onclick={() => showDictionary = !showDictionary}>
				{showDictionary ? 'Hide' : 'Show'} Word-for-Word Dictionary
			</button>

			{#if showDictionary}
				<div class="dictionary-table">
					<div class="dict-header">
						<span>Awadhi</span>
						<span>Sanskrit</span>
						<span>English</span>
					</div>
					{#each verse.word_meanings as entry}
						<div class="dict-row">
							<span class="devanagari">{entry.awadhi}</span>
							<span class="devanagari">{entry.sanskrit}</span>
							<span>{entry.english} 
								{#if entry.notes}<br/><small style="color: var(--primary);">{entry.notes}</small>{/if}
							</span>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.card-container {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.text-block {
		text-align: center;
	}

	.script-line {
		margin-bottom: 0.5rem;
		white-space: nowrap;
		overflow-x: auto;
		padding-bottom: 0.5rem;
	}

	.divider {
		border: 0;
		height: 1px;
		background: var(--glass-border);
		width: 50%;
		margin: 0 auto;
	}

	.english-meaning {
		font-size: 1.25rem;
		font-weight: 300;
		color: var(--text-main);
	}

	.dict-toggle {
		background: rgba(255,255,255,0.05);
		border: 1px solid var(--glass-border);
		color: var(--text-main);
		padding: 0.5rem 1rem;
		border-radius: 8px;
		cursor: pointer;
		font-family: var(--font-sans);
		transition: background 0.2s;
		width: 100%;
		font-size: 1rem;
	}
	.dict-toggle:hover {
		background: rgba(255,255,255,0.1);
	}

	.dictionary-table {
		margin-top: 1rem;
		background: var(--glass-bg);
		border-radius: 8px;
		overflow: hidden;
		text-align: left;
	}

	.dict-header {
		display: grid;
		grid-template-columns: 1fr 1fr 1.5fr;
		gap: 1rem;
		padding: 0.75rem 1rem;
		background: rgba(0,0,0,0.1);
		font-weight: 600;
		color: var(--text-muted);
		border-bottom: 1px solid var(--glass-border);
	}

	.dict-row {
		display: grid;
		grid-template-columns: 1fr 1fr 1.5fr;
		gap: 1rem;
		padding: 0.75rem 1rem;
		border-bottom: 1px solid rgba(255,255,255,0.02);
	}
	.dict-row:last-child {
		border-bottom: none;
	}
	.dict-row span {
		font-size: 1.1rem;
	}
</style>
