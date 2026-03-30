<script>
	let { box } = $props();

	/** @param {string} citation */
	function getIITKLink(citation) {
		if (!citation) return "https://www.valmiki.iitk.ac.in/";
		
		const kandaMap = {
			'Bala Kanda': 1,
			'Ayodhya Kanda': 2,
			'Aranya Kanda': 3,
			'Kishkindha Kanda': 4,
			'Sundara Kanda': 5,
			'Yuddha Kanda': 6,
			'Uttara Kanda': 7
		};

		let tid = null;
		for (const [name, id] of Object.entries(kandaMap)) {
			if (citation.includes(name)) {
				tid = id;
				break;
			}
		}

		const sargaMatch = citation.match(/(\d+):/);
		const sarga = sargaMatch ? sargaMatch[1] : null;

		if (tid && sarga) {
			return `https://www.valmiki.iitk.ac.in/sloka?field_kanda_tid=${tid}&language=dv&field_sarga_value=${sarga}`;
		}
		
		return "https://www.valmiki.iitk.ac.in/";
	}
</script>

<div class={`glass-card context-box type-${box.type}`}>
	
	<!-- ANCHOR BOX (Stories) -->
	{#if box.type === 'anchorbox'}
		<div class="box-header">
			<span class="icon">📖</span>
			<h3 class="title">{box.title}</h3>
		</div>
		<p class="description">{box.description}</p>
		
		{#if box.motivating_text || box.citation}
			<div class="citation-block">
				{#if box.motivating_text}
					<p class="motivating">"{box.motivating_text}"</p>
				{/if}
				{#if box.citation}
					<p class="citation">
						— <a href={getIITKLink(box.citation)} target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: underline; text-decoration-color: var(--primary); text-underline-offset: 4px;">
							Valmiki Ramayana, <em>{box.citation}</em>
						</a>
					</p>
				{/if}
			</div>
		{/if}
	
	<!-- GOTCHA BOX (Grammar) -->
	{:else if box.type === 'gotchabox'}
		<div class="box-header">
			<span class="icon">💡</span>
			<h3 class="title" style="color: #eab308;">Linguistic Notes</h3>
		</div>
		<ul class="gotcha-list">
			{#each box.items as item}
				<li>
					<!-- We can safely render markdown/latex-stripped bold here if needed, but it's raw text mostly -->
					{@html item.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}
				</li>
			{/each}
		</ul>

	<!-- APPRECIATION BOX (Poetry) -->
	{:else if box.type === 'appreciationbox'}
		<div class="box-header">
			<span class="icon">✨</span>
			<h3 class="title" style="color: #a855f7;">Poetic Brilliance</h3>
		</div>
		<p class="description">{@html box.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</p>
	{/if}
</div>

<style>
	.context-box {
		position: relative;
		overflow: hidden;
	}

	/* Subtle left borders indicating box type */
	.type-anchorbox {
		border-left: 4px solid var(--primary);
	}
	.type-gotchabox {
		border-left: 4px solid #eab308;
	}
	.type-appreciationbox {
		border-left: 4px solid #a855f7;
	}

	.box-header {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 1rem;
	}

	.icon {
		font-size: 1.5rem;
	}

	.title {
		margin: 0;
		color: var(--primary); /* Default for anchor */
		font-size: 1.25rem;
	}

	.description {
		font-size: 1.15rem;
		color: var(--text-main);
		line-height: 1.6;
		margin: 0;
	}

	.citation-block {
		margin-top: 1.5rem;
		padding-top: 1rem;
		border-top: 1px solid var(--glass-border);
	}

	.motivating {
		font-style: italic;
		margin: 1rem 0;
		color: var(--text-main);
	}

	.citation {
		text-align: right;
		font-size: 0.95rem;
		color: var(--text-main);
		font-weight: 600;
		margin: 0;
	}

	.gotcha-list {
		margin: 0;
		padding-left: 1.2rem;
		color: var(--text-main);
		font-size: 1.1rem;
	}
	.gotcha-list li {
		margin-bottom: 0.5rem;
	}
	:global(.gotcha-list strong) {
		color: var(--text-main);
	}
</style>
