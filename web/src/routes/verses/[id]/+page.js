export async function load({ params }) {
	try {
		const verseData = await import(`../../../lib/data/verses/${params.id}.json`);
		return { verse: verseData.default };
	} catch (e) {
		return { error: 'Verse not found' };
	}
}
