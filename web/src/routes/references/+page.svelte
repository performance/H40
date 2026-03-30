<script>
	import rawRefs from '$lib/data/references.md?raw';
	import { marked } from 'marked';

	const htmlContent = marked.parse(rawRefs);
</script>

<svelte:head>
	<title>Hanuman Chalisa | References</title>
</svelte:head>

<div class="glass-card prose">
	{@html htmlContent}
</div>
