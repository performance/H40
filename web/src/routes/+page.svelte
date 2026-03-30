<script>
	import rawIntro from '$lib/data/intro.md?raw';
	import { marked } from 'marked';

	const htmlContent = marked.parse(rawIntro);
</script>

<svelte:head>
	<title>Hanuman Chalisa | Introduction</title>
</svelte:head>

<div style="text-align: center; margin-bottom: 3rem;">
	<h1 style="font-size: 3.5rem; color: var(--primary); margin-bottom: 0.5rem;">Shri Hanuman Chalisa</h1>
	<p style="font-size: 1.3rem; color: var(--text-muted); max-width: 600px; margin: 0 auto;">A comprehensive linguistic, theological, and rhythmic guide.</p>
</div>

<div class="glass-card prose" style="max-width: 1000px;">
	{@html htmlContent}
</div>
