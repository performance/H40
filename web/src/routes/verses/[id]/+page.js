import index from '../../../lib/data/index.json';

export const prerender = true;

export function entries() {
	return index.map(v => ({ id: v.id }));
}

export async function load({ params }) {
	try {
		const verseData = await import(`../../../lib/data/verses/${params.id}.json`);
		return { verse: verseData.default };
	} catch (e) {
		return { error: 'Verse not found' };
	}
}
