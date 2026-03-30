<script>
	import glossaryData from '$lib/data/glossary.json';
</script>

<svelte:head>
	<title>Hanuman Chalisa | Glossary</title>
</svelte:head>

<div style="margin-bottom: 2rem;">
	<h1 style="font-size: 3rem; color: var(--primary);">Glossary of Divine Terms</h1>
	<p style="font-size: 1.2rem; color: var(--text-muted);">Deep structural definitions of theological lists compiled in the Chalisa.</p>
</div>

<div class="glossary-list">
	{#each glossaryData as block}
		<div class="glass-card section-card">
			<h2 style="color: var(--secondary); margin-bottom: 0.5rem;">{block.category} <span style="color: var(--text-muted); font-size: 1.2rem; font-weight: 300;">({block.sanskrit_name})</span></h2>
			<p style="margin-bottom: 1.5rem; font-size: 1.1rem;">{block.description}</p>
			
			<div class="items-grid">
				{#each block.items as item}
					<div class="item-card">
						<h3 style="color: var(--primary); margin-bottom: 0.25rem;">{item.name.replace(/\*\*/g, '')} <span class="devanagari" style="font-size: 1.2rem; color: var(--text-devanagari);">{item.sanskrit}</span></h3>
						<p style="margin: 0; color: var(--text-main);">{item.description}</p>
					</div>
				{/each}
			</div>
		</div>
	{/each}
</div>

<style>
	.glossary-list {
		display: flex;
		flex-direction: column;
		gap: 3rem;
	}

	.items-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 1.5rem;
	}

	.item-card {
		background: rgba(0, 0, 0, 0.05);
		border-radius: 8px;
		padding: 1.25rem;
		border-left: 4px solid var(--primary);
	}
</style>
