<script>
	import '../app.css';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import NextPrevNav from '$lib/components/NextPrevNav.svelte';
	let { children } = $props();

	let theme = $state('dark');

	onMount(() => {
		theme = localStorage.getItem('theme') || 'dark';
		document.documentElement.setAttribute('data-theme', theme);
	});

	function toggleTheme() {
		theme = theme === 'dark' ? 'light' : 'dark';
		document.documentElement.setAttribute('data-theme', theme);
		localStorage.setItem('theme', theme);
	}
</script>

<nav class="nav-header">
	<a href="/" class="logo" style="font-size: 1.5rem; font-weight: 800; color: var(--text-main); text-decoration: none;">
		Hanuman <span style="color: var(--primary);">Chalisa</span>
	</a>
	<div class="nav-links">
		<a href="/" class:active={$page.url.pathname === '/'}>Introduction</a>
		<a href="/verses" class:active={$page.url.pathname === '/verses' || $page.url.pathname.startsWith('/verses/')}>Verses</a>
		<a href="/glossary" class:active={$page.url.pathname === '/glossary'}>Glossary</a>
		<button class="theme-toggle" onclick={toggleTheme} aria-label="Toggle structural theme">
			{theme === 'dark' ? '☀️' : '🌙'}
		</button>
		<a href="/Hanuman_Chalisa_Study_Guide.pdf" class="download-btn" target="_blank" rel="noopener noreferrer">
			📥 PDF Book
		</a>
	</div>
</nav>

<style>
	.theme-toggle {
		background: none;
		border: 1px solid var(--glass-border);
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 40px;
		height: 40px;
		cursor: pointer;
		font-size: 1.2rem;
		margin-left: 1rem;
		transition: background 0.2s ease;
	}
	.theme-toggle:hover {
		background: var(--glass-bg);
	}
	.download-btn {
		background: var(--primary);
		color: #fff !important;
		padding: 0.5rem 1rem;
		border-radius: 8px;
		font-weight: 700;
		text-decoration: none !important;
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		margin-left: 0.5rem;
		transition: background 0.2s ease, transform 0.2s ease;
	}
	.download-btn:hover {
		background: #ea580c;
		transform: translateY(-2px);
	}
</style>

<main style="padding: 2rem; max-width: 1600px; margin: 0 auto; min-height: 80vh;">
	<NextPrevNav position="top" />
	{@render children()}
	<NextPrevNav position="bottom" />
</main>
