<script>
	import VerseCard from '$lib/components/VerseCard.svelte';
	import RhythmMap from '$lib/components/RhythmMap.svelte';
	import ContextBox from '$lib/components/ContextBox.svelte';
	import { base } from '$app/paths';

	let { data } = $props();
	let verse = $derived(data.verse);
</script>

<svelte:head>
	<title>Hanuman Chalisa | {verse ? verse.title : 'Error'}</title>
</svelte:head>

{#if data.error}
	<div class="glass-card" style="text-align: center; margin-top: 4rem;">
		<h1 style="color: var(--primary);">Verse Not Found</h1>
		<p>The requested verse could not be loaded.</p>
		<a href="{base}/" style="display: inline-block; margin-top: 1rem;">Return Home</a>
	</div>
{:else}
	<div class="verse-layout">
		<header class="verse-header">
			<a href="{base}/verses" class="back-link">← Index</a>
			<h1 class="verse-title" style="font-family: var(--font-deva); font-size: 2.2rem;">{verse.title}</h1>
			<div></div>
		</header>

		<!-- Main Verse Text & Translations -->
		<VerseCard {verse} />

		<!-- Visual Rhythm Map -->
		{#if verse.rhythm_map && verse.rhythm_map.length > 0}
			<RhythmMap map={verse.rhythm_map} />
		{/if}

		<!-- Semantic Boxes (Anecdotes, Gotchas) -->
		{#if verse.boxes && verse.boxes.length > 0}
			<div class="boxes-container">
				{#each verse.boxes as box}
					<ContextBox {box} />
				{/each}
			</div>
		{/if}
	</div>
{/if}

<style>
	.verse-layout {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		max-width: 1400px;
		margin: 0 auto;
	}

	.verse-header {
		display: grid;
		grid-template-columns: 1fr auto 1fr;
		align-items: center;
		border-bottom: 1px solid var(--glass-border);
		padding-bottom: 1rem;
	}

	.verse-title {
		margin: 0;
		text-transform: capitalize;
		color: var(--secondary);
		text-align: center;
	}

	.back-link {
		color: var(--text-muted);
		font-weight: 600;
		justify-self: start;
	}
	
	@media (max-width: 600px) {
		.verse-header {
			grid-template-columns: 1fr;
			gap: 1.5rem;
			justify-items: center;
		}
		.back-link {
			justify-self: center;
		}
	}

	.boxes-container {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		margin-top: 1rem;
	}
</style>
