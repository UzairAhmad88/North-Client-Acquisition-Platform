export type LeadStatus="NEW"|"RESEARCHING"|"QUALIFIED"|"CONTACTED"|"RESPONDED"|"INTERESTED"|"MEETING"|"PROPOSAL"|"WON"|"FOLLOW_UP"|"NOT_INTERESTED"|"LOST";
export interface Business{id:string;name:string;website?:string;city?:string;category?:string}
export interface Lead{id:string;business_id:string;status:LeadStatus;priority:string}
