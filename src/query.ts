export type JSONRecord = Record<string, any>;

export default abstract class GQLQuery {
    abstract name: string;
    abstract query: string;
    abstract endpoint: string;
    id: string;

    constructor(id: string) {
        this.id = id;
    }

    abstract get variables(): JSONRecord

    private async sha256Query(): Promise<string> {
        const msgBuffer = new TextEncoder().encode(this.query);
        const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
        return hashHex;
    }

    public async getExtensions(): Promise<JSONRecord> {
        return {
            persistedQuery: {
                version: 1,
                sha256Hash: await this.sha256Query()
            }
        }
    }

    public parseResponse(json: JSONRecord): JSONRecord {
        return json;
    }
}
