<script>
	import rawIntro from '$lib/data/intro.md?raw';
	import { marked } from 'marked';

	const htmlContent = marked.parse(rawIntro);
</script>

<svelte:head>
	<title>Hanuman Chalisa | Introduction</title>
</svelte:head>

<div style="text-align: center; margin-bottom: 3rem;">
	<h1 style="font-size: clamp(1.8rem, 6vw, 2.5rem); color: var(--primary); margin-bottom: 0.5rem; line-height: 1.3;">
		श्री हनुमान चालीसा<br/>
		శ్రీ హనుమాన చాలీసా<br/>
		śrī hanumān cālīsā
	</h1>
	<p style="font-size: 1.3rem; color: var(--text-muted); max-width: 600px; margin: 0 auto; line-height: 1.4;">
		A Linguistic & Structural Study Guide<br/>
		<span style="font-size: 1rem; opacity: 0.8;">Compiled for easy learning</span>
	</p>
</div>

<div class="glass-card prose" style="max-width: 1000px;">
	{@html htmlContent}
</div>
