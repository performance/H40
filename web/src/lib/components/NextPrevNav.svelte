<script>
	import indexData from '$lib/data/index.json';
	import { page } from '$app/stores';

	let { position = 'bottom' } = $props();

	let navList = [
		{ path: '/', title: 'Introduction' },
		...indexData.map(v => ({ 
			path: `/verses/${v.id}`, 
			title: v.id.replace('chaupai', 'Chaupai ').replace('doha', 'Doha ').replace('concluding_Doha ', 'Concluding Doha') 
		})),
		{ path: '/glossary', title: 'Glossary' },
		{ path: '/references', title: 'References' }
	];

	let currentIndex = $derived(navList.findIndex(item => item.path === $page.url.pathname));
	let prev = $derived(currentIndex > 0 ? navList[currentIndex - 1] : null);
	let next = $derived(currentIndex !== -1 && currentIndex < navList.length - 1 ? navList[currentIndex + 1] : null);
</script>

<div class={`pagination-nav ${position}`}>
	{#if prev}
		<a href={prev.path} class="glass-card nav-button prev">
			<span class="arrow">←</span>
			<span class="text">
				<small>Previous</small>
				<strong style="text-transform: capitalize;">{prev.title}</strong>
			</span>
		</a>
	{:else}
		<div></div>
	{/if}

	{#if next}
		<a href={next.path} class="glass-card nav-button next">
			<span class="text">
				<small>Next</small>
				<strong style="text-transform: capitalize;">{next.title}</strong>
			</span>
			<span class="arrow">→</span>
		</a>
	{/if}
</div>

<style>
	.pagination-nav {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
	}

	.pagination-nav.bottom {
		margin-top: 4rem;
		padding-top: 2rem;
		border-top: 1px solid var(--glass-border);
	}

	.pagination-nav.top {
		margin-bottom: 2rem;
		padding-bottom: 2rem;
		border-bottom: 1px solid var(--glass-border);
	}

	.nav-button {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1rem 1.5rem;
		text-decoration: none;
		color: var(--text-main);
		flex: 1;
		max-width: 350px;
	}

	.nav-button.prev {
		text-align: left;
	}

	.nav-button.next {
		text-align: right;
		justify-content: flex-end;
		margin-left: auto;
	}

	.text {
		display: flex;
		flex-direction: column;
	}

	.text small {
		color: var(--text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		font-size: 0.8rem;
		margin-bottom: 0.2rem;
	}

	.text strong {
		color: var(--primary);
		font-size: 1.2rem;
	}

	.arrow {
		font-size: 1.5rem;
		color: var(--text-muted);
		transition: transform 0.2s ease, color 0.2s ease;
	}

	.nav-button:hover .arrow {
		color: var(--primary);
	}

	.nav-button.prev:hover .arrow {
		transform: translateX(-4px);
	}

	.nav-button.next:hover .arrow {
		transform: translateX(4px);
	}
</style>
