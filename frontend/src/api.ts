export type Concept = {id:string; title:string; prerequisites:string[]; description:string};
export type Mastery = {concept_id:string; score:number; attempts:number; correct_count:number; next_review_at:string|null; status:'unassessed'|'assessed'};
export type Question = {id:string;concept_id:string;difficulty:string;prompt:string;options:string[]};
export type Feedback = {correct:boolean;correct_option:number;explanation:string;coach_tip:string;mastery_before:number;mastery_after:number;misconception:string|null;reasoning_quality:string;analysis_mode:string;confidence:string;next_review_at:string;next_question:Question};
export type Profile = {student:{id:string;name:string};mastery:Mastery[]};
export type Analytics = {demo_data:boolean;total_learners:number;concepts:{concept_id:string;title:string;avg_mastery:number|null;assessed:number}[];misconceptions:{label:string;count:number}[];learners:{name:string;assessed:number;avg_mastery:number|null}[]};
const BASE = import.meta.env.VITE_API_BASE_URL || '';
export async function api<T>(path:string, options?:RequestInit):Promise<T>{
  const response = await fetch(`${BASE}${path}`, {headers:{'Content-Type':'application/json'},...options});
  if (!response.ok) {let message = `Request failed (${response.status})`;try {const body=await response.json();message=body.detail||message;}catch{/* preserve HTTP status */}throw new Error(message);}
  return response.json() as Promise<T>;
}
