<script>
	import indexData from '$lib/data/index.json';
</script>

<svelte:head>
	<title>Hanuman Chalisa | Verse Index</title>
</svelte:head>

<div style="text-align: center; margin-bottom: 3rem;">
	<h1 style="font-size: 3rem; color: var(--primary);">Index of Verses</h1>
	<p style="font-size: 1.2rem; color: var(--text-muted);">Explore the visual rhythm, grammar, and profound meaning of every verse.</p>
</div>

<div class="grid">
	{#each indexData as verse}
		<a href={`/verses/${verse.id}`} class="glass-card verse-link">
			<div class="type-badge">{verse.id.replace('chaupai', 'Chaupai ').replace('doha', 'Doha ').replace('concluding_Doha ', 'Concluding Doha')}</div>
			<div class="arrow">→</div>
		</a>
	{/each}
</div>

<style>
	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
		gap: 1.5rem;
	}

	.verse-link {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1.5rem;
		cursor: pointer;
	}

	.type-badge {
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--text-main);
		text-transform: capitalize;
	}

	.arrow {
		font-size: 1.5rem;
		color: var(--primary);
		transition: transform 0.2s ease;
	}

	.verse-link:hover .arrow {
		transform: translateX(4px);
	}
</style>
